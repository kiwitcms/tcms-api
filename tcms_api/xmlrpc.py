"""
XMLRPC driver

Use this class to access Kiwi TCMS via XML-RPC
This code is based on
http://landfill.bugzilla.org/testopia2/testopia/contrib/drivers/python/testopia.py
and https://fedorahosted.org/python-bugzilla/browser/bugzilla/base.py

History:
2011-12-31 bugfix https://bugzilla.redhat.com/show_bug.cgi?id=735937
"""
# pylint: disable=too-few-public-methods

from http import HTTPStatus
from http.client import HTTPSConnection
from http.cookiejar import CookieJar
import urllib.parse
from xmlrpc.client import SafeTransport, Transport, ServerProxy
import sys

import requests

if sys.platform.startswith("win"):
    import winkerberos as kerberos  # pylint: disable=import-error
else:
    import kerberos  # pylint: disable=import-error

VERBOSE = 0


class CookieTransport(Transport):
    """A subclass of xmlrpc.client.Transport that supports cookies."""
    cookiejar = None
    scheme = 'http'

    def __init__(self, use_datetime=False, use_builtin_types=False):
        super().__init__(use_datetime, use_builtin_types)
        self.cookiejar = CookieJar()
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
    scheme = 'https'


# Taken from FreeIPA source freeipa-1.2.1/ipa-python/krbtransport.py
class KerbTransport(SafeCookieTransport):
    """Handles Kerberos Negotiation authentication to an XML-RPC server."""

    def get_host_info(self, host):
        host, extra_headers, x509 = Transport.get_host_info(self, host)

        # Set the remote host principal
        hostinfo = host.split(':')
        service = "HTTP@" + hostinfo[0]

        _result, context = kerberos.authGSSClientInit(service)
        kerberos.authGSSClientStep(context, "")

        extra_headers = [
            ("Authorization", "Negotiate %s" %
             kerberos.authGSSClientResponse(context))
        ]

        return host, extra_headers, x509

    def make_connection(self, host):
        """
        For fixing https://bugzilla.redhat.com/show_bug.cgi?id=735937

        Return an individual HTTPS connection for each request.
        """
        chost, self._extra_headers, x509 = self.get_host_info(host)
        # Kiwi TCMS isn't ready to use HTTP/1.1 persistent connections,
        # so tell server current opened HTTP connection should be closed after
        # request is handled. And there will be a new connection for the next
        # request.
        self._extra_headers.append(('Connection', 'close'))
        self._connection = host, HTTPSConnection(  # nosec:B309:blacklist
            chost,
            None,
            **(x509 or {})
        )
        return self._connection[1]


def get_hostname(url):
    """
        Performs the same parsing of the URL as the Transport
        class and returns only the hostname which is used to
        generate the service principal name for Kiwi TCMS and
        the respective Authorize header!
    """
    _type, uri = urllib.parse.splittype(url)
    hostname, _path = urllib.parse.splithost(uri)
    return hostname


class TCMSXmlrpc:
    """
    TCMS XML-RPC client for server deployed without BASIC authentication.
    """
    def __init__(self, username, password, url):
        if url.startswith('https://'):
            self.transport = SafeCookieTransport()
        elif url.startswith('http://'):
            self.transport = CookieTransport()
        else:
            raise Exception("Unrecognized URL scheme")

        self.server = ServerProxy(
            url,
            transport=self.transport,
            verbose=VERBOSE,
            allow_none=1
        )

        # Login, get a cookie into our cookie jar (login_dict):
        self.server.Auth.login(username, password)


class TCMSKerbXmlrpc(TCMSXmlrpc):
    """
    TCMSXmlrpc - TCMS XML-RPC client
                    for server deployed with mod_auth_kerb
    """
    session_cookie_name = 'sessionid'

    def __init__(self, url):  # pylint: disable=super-init-not-called
        if url.startswith('https://'):
            self.transport = KerbTransport()
        elif url.startswith('http://'):
            raise Exception("Encrypted https communication required for "
                            "Kerberos authentication."
                            "URL provided: {0}".format(url))
        else:
            raise Exception("Unrecognized URL scheme: {0}".format(url))

        self.server = ServerProxy(
            url,
            transport=self.transport,
            verbose=VERBOSE,
            allow_none=1
        )

        # Login, get a cookie into our cookie jar (login_dict):
        self.login(url)

    def login(self, url):
        url = url.replace('xml-rpc', 'login/kerberos')
        hostname = get_hostname(url)

        _, headers, _ = self.transport.get_host_info(hostname)
        # transport returns list of tuples but requests needs a dictionary
        headers = dict(headers)

        # note: by default will follow redirects
        with requests.sessions.Session() as session:
            response = session.get(url, headers=headers)
            assert response.status_code == HTTPStatus.OK
            self.transport._cookies.append(  # pylint: disable=protected-access
                self.session_cookie_name + '=' +
                session.cookies[self.session_cookie_name]
            )
