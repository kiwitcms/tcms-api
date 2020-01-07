Python API for Kiwi TCMS
========================

.. image:: https://travis-ci.org/kiwitcms/tcms-api.svg?branch=master
    :target: https://travis-ci.org/kiwitcms/tcms-api

.. image:: https://readthedocs.org/projects/tcms-api/badge/?version=latest
    :target: http://tcms-api.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation

.. image:: https://coveralls.io/repos/github/kiwitcms/tcms-api/badge.svg?branch=master
    :target: https://coveralls.io/github/kiwitcms/tcms-api?branch=master
    :alt: Code coverage

.. image:: https://tidelift.com/badges/package/pypi/tcms-api
    :target: https://tidelift.com/subscription/pkg/tcms-api?utm_source=pypi-tcms-api&utm_medium=github&utm_campaign=readme
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


CHANGELOG
---------

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
- Copyright (c) 2017-2019 Kiwi TCMS Project and its contributors. All rights reserved.

This library is free software; you can redistribute it and/or
modify it under the terms of the GNU Lesser General Public
License as published by the Free Software Foundation; either
version 2.1 of the License, or (at your option) any later version.
