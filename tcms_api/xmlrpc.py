# pylint: disable=protected-access,too-few-public-methods,invalid-name,attribute-defined-outside-init

import sys
import urllib.parse

from base64 import b64encode
from datetime import datetime, timedelta
from http import HTTPStatus
from http.client import HTTPSConnection
from xmlrpc.client import _Method, SafeTransport, Transport, ServerProxy

try:
    import gssapi
except ImportError:
    gssapi = None

import requests

from tcms_api.version import __version__


VERBOSE = 0
_PYTHON_VERSION = sys.version.replace("\n", "")


class TCMSProxy(ServerProxy):
    _connected_since = datetime(2024, 1, 1, 0, 0)

    def __request(self, methodname, params):
        # refresh the connection every 4 minutes to avoid an
        # `ssl.SSLEOFError: EOF occurred in violation of protocol` error with Python >= 3.10
        # In practice I've discovered that 5 minutes works as well, 6 minutes fails so
        # be more cautious and refresh the connection earlier!
        #
        # Side note: originally I thought this is related to calling
        # context.set_alpn_protocols(['http/1.1']) inside http/client.py, introduced in
        # https://github.com/python/cpython/commit/f97406be4c0a02c1501c7ab8bc8ef3850eddb962
        # but that doesn't seem to be the case (or is much harder for me to debug)!
        if getattr(
            self._ServerProxy__transport,  # pylint: disable=access-member-before-definition
            "internal_refresh",
            False,
        ) and datetime.now() - self._connected_since > timedelta(minutes=4):
            self._ServerProxy__transport = self._ServerProxy__transport.__class__()
            self._connected_since = datetime.now()

        self._ServerProxy__transport._extra_headers = [("Referer", methodname)]
        return self._ServerProxy__request(methodname, params)

    def __getattr__(self, name):
        return _Method(self.__request, name)


class CookieTransport(Transport):
    """A subclass of xmlrpc.client.Transport that supports cookies."""

    scheme = "http"
    user_agent = f"tcms-api/{__version__}/Python {_PYTHON_VERSION}"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cookies = []

    def send_headers(self, connection, headers):
        if self._cookies:
            connection.putheader("Cookie", "; ".join(self._cookies))
        super().send_headers(connection, headers)

    def parse_response(self, response):
        for header in response.msg.get_all("Set-Cookie", []):
            cookie = header.split(";", 1)[0]
            self._cookies.append(cookie)
        return super().parse_response(response)


class SafeCookieTransport(SafeTransport, CookieTransport):
    """SafeTransport subclass that supports cookies."""

    internal_refresh = True
    scheme = "https"


class KerbTransport(SafeCookieTransport):
    """Handles GSSAPI Negotiation (SPNEGO) authentication."""

    internal_refresh = False

    def get_host_info(self, host):
        host, extra_headers, x509 = Transport.get_host_info(self, host)

        # Set the remote host principal
        hostinfo = host.split(":")
        service = "HTTP@" + hostinfo[0]

        service_name = gssapi.Name(service, gssapi.NameType.hostbased_service)
        context = gssapi.SecurityContext(usage="initiate", name=service_name)
        token = context.step()
        token = b64encode(token).decode()
        extra_headers = [("Authorization", f"Negotiate {token}")]

        return host, extra_headers, x509

    def make_connection(self, host):
        """
        Return an individual HTTPS connection for each request.

        Fix https://bugzilla.redhat.com/show_bug.cgi?id=735937
        """
        chost, self._extra_headers, x509 = self.get_host_info(host)
        # Kiwi TCMS isn't ready to use HTTP/1.1 persistent connections,
        # so tell server current opened HTTP connection should be closed after
        # request is handled. And there will be a new connection for the next
        # request.
        self._extra_headers.append(("Connection", "close"))
        self._connection = host, HTTPSConnection(  # nosec:B309:blacklist
            chost, None, **(x509 or {})
        )
        return self._connection[1]


def get_hostname(url):
    """
    Performs the same parsing of the URL as the Transport
    class and returns only the hostname which is used to
    generate the service principal name for Kiwi TCMS and
    the respective Authorize header!
    """
    result = urllib.parse.urlparse(url)
    return result.netloc


class TCMSXmlrpc:
    """
    XML-RPC client for username/password authentication.
    """

    session_cookie_name = "sessionid"
    transport = None

    def __init__(self, username, password, url):
        if self.transport is None:
            if url.startswith("https://"):
                self.transport = SafeCookieTransport()
            elif url.startswith("http://"):
                self.transport = CookieTransport()
            else:
                raise RuntimeError("Unrecognized URL scheme")

        self.server = TCMSProxy(
            url, transport=self.transport, verbose=VERBOSE, allow_none=1
        )

        self.username = username
        self.password = password
        self.url = url

        self.login()

    def login(self):
        # note: do not override .login()
        self._do_login()

    def _do_login(self):
        """
        Login in the web app to save a session cookie in the cookie jar!
        """
        self.server.Auth.login(self.username, self.password)


class TCMSKerbXmlrpc(TCMSXmlrpc):
    """
    XML-RPC client for server deployed with python-social-auth-kerberos.

    Should also work for servers deployed with mod_auth_gssapi but
    that is not supported nor guaranteed!
    """

    transport = KerbTransport()

    def __init__(self, username, password, url):
        if not url.startswith("https://"):
            raise RuntimeError(
                f"https:// required for GSSAPI authentication. URL provided: {url}"
            )

        if gssapi is None:
            raise RuntimeError("gssapi not found! Try pip install tcms-api[gssapi]")

        super().__init__(username, password, url)

    def _do_login(self):
        url = self.url.replace("xml-rpc", "login/kerberos")
        hostname = get_hostname(url)

        _, headers, _ = self.transport.get_host_info(hostname)
        # transport returns list of tuples but requests needs a dictionary
        headers = dict(headers)
        headers["User-Agent"] = self.transport.user_agent

        # note: by default will follow redirects
        with requests.sessions.Session() as session:
            response = session.get(url, headers=headers)
            assert response.status_code == HTTPStatus.OK
            self.transport._cookies.append(  # pylint: disable=protected-access
                self.session_cookie_name
                + "="
                + session.cookies[self.session_cookie_name]
            )
