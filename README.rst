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
For more information see
http://kiwitcms.readthedocs.io/en/latest/api/index.html.


INSTALLATION
------------

::

    pip install tcms-api

**WARNING:** on Windows you need to install MIT Kerberos and make sure
``C:\Program Files\MIT\Kerberos\bin`` is included in ``%PATH%`` -
this is usually the case when you install and restart! It must be
a 64bit installation, see
`MIT Kerberos for Windows 4.1 <https://web.mit.edu/kerberos/dist/index.html#kfw-4.1>`_


CHANGELOG
---------

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
- Copyright (c) 2017-2020 Kiwi TCMS Project and its contributors. All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
