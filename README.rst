Python API for Kiwi TCMS
========================

.. image:: https://travis-ci.org/kiwitcms/tcms-api.svg?branch=master
    :target: https://travis-ci.org/kiwitcms/tcms-api

.. image:: https://ci.appveyor.com/api/projects/status/jhuyyt9vrpaxagrk?svg=true
    :target: https://ci.appveyor.com/project/atodorov/tcms-api

.. image:: https://readthedocs.org/projects/tcms-api/badge/?version=latest
    :target: http://tcms-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation

.. image:: https://codecov.io/gh/kiwitcms/tcms-api/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/kiwitcms/tcms-api
    :alt: Code coverage

.. image:: https://tidelift.com/badges/package/pypi/tcms-api
    :target: https://tidelift.com/subscription/pkg/pypi-tcms-api?utm_source=pypi-tcms-api&utm_medium=github&utm_campaign=readme
    :alt: Tidelift

.. image:: https://opencollective.com/kiwitcms/tiers/sponsor/badge.svg?label=sponsors&color=brightgreen
   :target: https://opencollective.com/kiwitcms#contributors
   :alt: Become a sponsor

.. image:: https://img.shields.io/twitter/follow/KiwiTCMS.svg
    :target: https://twitter.com/KiwiTCMS
    :alt: Kiwi TCMS on Twitter


This package allows to connect and access Kiwi TCMS API.


DOCUMENTATION
-------------

https://tcms-api.readthedocs.io/en/latest/modules/tcms_api.html


CHANGELOG
---------

v13.3 (10 Jun 2024)
~~~~~~~~~~~~~~~~~~~

- Update requirements and imports for the ``strtobool()`` function


v13.2 (27 Apr 2024)
~~~~~~~~~~~~~~~~~~~

- Respect configuration passed as arguments to the ``TCMS()`` class, for example::

    TCMS("https://kiwitcms.example.com/xml-rpc/", "api-bot", "keep-me-secret")

- Adjust usage examples and documentation for ``.exec()``. Closes
  `Issue #77 <https://github.com/kiwitcms/tcms-api/issues/77>`_
- Internal changes related to testing and building this package


v12.9.1 (13 Jan 2024)
~~~~~~~~~~~~~~~~~~~~~

- Refactor RPC connection refresh using a proxy-class pattern which also
  takes care to call ``.login()`` upon refresh


v12.9 (12 Jan 2024)
~~~~~~~~~~~~~~~~~~~

- Refresh internal https transport every 4 minutes to avoid an
  ``ssl.SSLEOFError: EOF occurred in violation of protocol`` error
  on Python 3.10 and later when executing very long running tests.
  Limited to non-kerberos connections!
- Include Python version in ``User-Agent`` header
- Send XML-RPC method name in ``Referer:`` header to improve logs


v12.8.2 (23 Dec 2023)
~~~~~~~~~~~~~~~~~~~~~

- Refactor calling ``.login()`` method as part of ``__init__`` again
  because the entire Kiwi TCMS test suite depends on this behavior


v12.8.1 (22 Dec 2023)
~~~~~~~~~~~~~~~~~~~~~

- Limit TestPlan.name and TestCase.summary length before any usage
  avoiding possible records mismatch between filter & create operations


v12.8 (17 Dec 2023)
~~~~~~~~~~~~~~~~~~~

- When creating a TestPlan limit name to 255 characters
- When creating a TestCase limit summary to 255 characters


v12.7 (10 Dec 2023)
~~~~~~~~~~~~~~~~~~~

- Build & test this package with Python 3.11
- Replace ``urllib.parse`` functions deprecated since Python 3.8
- Refactor issues reported by newer version of pylint
- Refactor issues reported by CodeQL
- Reformat source code with Black
- Enable ReadTheDocs CI


v12.2 (04 Apr 2023)
~~~~~~~~~~~~~~~~~~~

- New arguments for ``plugin_helpers.Backend.update_test_execution()`` method.
  Now accepts the ``start_date`` and ``stop_date`` arguments at the end of its
  signature
- Start testing the client library with Python 3.9


v11.4 (15 Jul 2022)
~~~~~~~~~~~~~~~~~~~

- Fallback to C:\tcms.conf in case we're on Windows
- [pre-commit.ci] pre-commit autoupdate


v11.3 (17 May 2022)
~~~~~~~~~~~~~~~~~~~

- Make it possible for plugins to print info about created/reused TP/TR
- Specify start_date when creating a TestRun


v11.2 (15 May 2022)
~~~~~~~~~~~~~~~~~~~

- Make plugin prefix configurable via ``TCMS_PREFIX`` environment variable.
  Fixes `Issue #6 <https://github.com/kiwitcms/tcms-api/issues/6>`_
- Use ``TCMS_PARENT_PLAN`` environment variable if specified. Will configure
  a parent TestPlan. Fixes
  `Issue #4 <https://github.com/kiwitcms/tcms-api/issues/4>`_
- Introduce ``plugin_helpers.Backend.name`` and
  ``plugin_helpers.Backend.version`` attributes
- Convert ``plugin_helpers.Backend.default_tester_id`` into a cached property
- Use the account sending the API request if ``default_tester_id`` is None.
  That avoide the use of ``User.filter`` API method for which most users may
  not be authorized
- Sanity check and sanitize URL config. Refs
  `Issue #45 <https://github.com/kiwitcms/tcms-api/issues/45>`_


v11.1 (13 May 2022)
~~~~~~~~~~~~~~~~~~~

- Allow the environment variable ``TCMS_DEFAULT_TESTER_ID`` to override
  internal queries, pointing directly to the user who will create new
  test plans, test runs and update test executions.
- Internal updates around CI


v11.0 (05 Dec 2021)
~~~~~~~~~~~~~~~~~~~

**WARNING:** contains backwards incompatible changes!

- Method ``plugin_helpers.Backend.add_test_case_to_run()`` now returns a list
- Adjust internal API calls for upcoming Kiwi TCMS v11.0
- Still compatible with Kiwi TCMS v10.x API
- Start using f-strings. Available since Python 3.6 which is the minimum
  required version for ``tcms-api`` anyway


v10.0 (02 March 2021)
~~~~~~~~~~~~~~~~~~~~~

**WARNING:** contains backwards incompatible changes!

- Compatible with Kiwi TCMS v10.0 or later


v9.0 (12 January 2021)
~~~~~~~~~~~~~~~~~~~~~~

**WARNING:** contains backwards incompatible changes!

- Compatible with Kiwi TCMS v9.0 or later
- Method ``Backend.build_id()`` doesn't receive ``product_id`` as firsts
  parameter anymore! Related to Kiwi TCMS
  `Issue #246 <https://github.com/kiwitcms/Kiwi/issues/246>`_


v8.6.0 (28 October 2020)
~~~~~~~~~~~~~~~~~~~~~~~~

- Use a sub-package to install gssapi, see installation instructions


v8.5.0 (04 August 2020)
~~~~~~~~~~~~~~~~~~~~~~~

- Fix ``super()`` call in ``CookieTransport`` class to make this package
  compatible with Python 3.8 (Václav Klikar)


v8.4.0 (25 June 2020)
~~~~~~~~~~~~~~~~~~~~~

- Add instructions how to install ``gssapi`` because they don't ship binary
  packages on Linux
- Provide ``plugin_helpers.Backend.get_statuses_by_weight()`` and fall-back
  to it if TestExecutionStatus can't be found by name. This is to be used
  by Kiwi TCMS plugins (Bryan Mutai)


v8.3.0 (10 April 2020)
~~~~~~~~~~~~~~~~~~~~~~

- Use ``gssapi`` library for kerberos communications on both Linux and Windows
- Requires MIT Kerberos for Windows, see installation instructions


v8.2.0 (02 April 2020)
~~~~~~~~~~~~~~~~~~~~~~

This version adds additional methods and functionality that can be used
by Kiwi TCMS plugins written in Python.

- Modify ``plugin_helpers.Backend.test_case_get_or_create()`` to return
  tuple (dict, bool). WARNING: this will break existing plugins
- ``plugin_helpers.Backend`` will use ``TCMS_PLAN_ID`` environment variable
  if specified. This allows the user to select an existing TestPlan to save
  new results into. Fixes
  `Issue #5 <https://github.com/kiwitcms/tcms-api/issues/5>`_
- Add ``plugin_helpers.Backend.finish_test_run()`` which may be
  called by plugins to indicate that a TestRun has been finished
- Add ``plugin_helpers.Backend.default_tester_id()`` and update
  ``TestExecution.tested_by`` when changing status
- Use ``default_tester_id()`` when creating a new TestRun
- When creating new test run always set TR.manager := TP.author
  and make sure that ``TestPlan.create()`` will also specify author


v8.1.1 (23 March 2020)
~~~~~~~~~~~~~~~~~~~~~~

- Use ``winkerberos`` dependency on Microsoft Windows platform
  (@mtg-edmund-tse)
- Setting rename in config file: ``use_mod_kerb`` -> ``use_kerberos``
- Bug-fix: don't fall back to user/pass if kerberos is configured
- Bug-fix: send correctly formatted authorization request header,
  per RFC-4459
- Bug-fix: properly authenticate with Kiwi TCMS via kerberos ticket
  if requested to do so
- Start sending ``User-Agent: tcms-api/<version>`` for all requests
- Enable integration testing with and without Kerberos
- Enable testing on Windows



v8.0.1 (10 February 2020)
~~~~~~~~~~~~~~~~~~~~~~~~~

This version is compatible only with Kiwi TCMS v8.0 or later!

- Do not use deprecated field ``product`` in ``TestCase.create`` API
  method
- Set ``TestCase.is_automated`` to ``True``



v8.0 (09 February 2020)
~~~~~~~~~~~~~~~~~~~~~~~

This version is compatible only with Kiwi TCMS v8.0 or later!

- Adjusts ``plugin_helpers`` module to reflect backwards incompatible
  API changes introduced in Kiwi TCMS v8.0



v6.7.1 (07 February 2020)
~~~~~~~~~~~~~~~~~~~~~~~~~

- Fix a bug in how ``use_mod_kerb`` setting was evaluated which
  lead to always preferring Kerberos which in turn was causing
  issues on Windows.



v6.7 (10 April 2019)
~~~~~~~~~~~~~~~~~~~~

This version is compatible only with Kiwi TCMS v6.7 or later!
For older server versions use tcms-api==5.3!

This version contains breaking changes in ``plugin_helpers``!

- Switch from ``TestCaseRun`` to ``TestExecution`` API. Fixes
  `Issue #7 <https://github.com/kiwitcms/tcms-api/issues/7>`_
- Rename ``plugin_helpers.Backend.update_test_case_run()`` to
  ``plugin_helpers.Backend.update_test_execution()``



COPYRIGHT
---------

- Copyright (c) 2012 Red Hat, Inc. All rights reserved.
- Copyright (c) 2017-2023 Kiwi TCMS Project and its contributors. All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
