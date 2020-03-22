#!/usr/bin/env python
import os
from setuptools import setup


def get_version():
    version = open(os.path.join('tcms_api', 'version.py')).read()
    return version.replace(
        ' ', ''
    ).replace('__version__=', '').strip().strip("'").strip('"')


def get_install_requires(path):
    requires = []

    with open(path, 'r') as file:
        for line in file:
            if line.startswith('-r '):
                continue
            requires.append(line.strip())
        return requires


with open("README.rst") as readme:
    LONG_DESCRIPTION = readme.read()


setup(name='tcms-api',
      version=get_version(),
      packages=['tcms_api'],
      description='Python API for Kiwi',
      long_description=LONG_DESCRIPTION,
      long_description_content_type="text/x-rst",
      maintainer='Kiwi TCMS',
      maintainer_email='info@kiwitcms.org',
      license='LGPLv2+',
      url='https://github.com/kiwitcms/tcms-api',
      python_requires='>=3.6',
      install_requires=get_install_requires('requirements.txt'),
      classifiers=[
          'Development Status :: 5 - Production/Stable',
          'Environment :: Console',
          'Intended Audience :: Developers',
          'Intended Audience :: System Administrators',
          'License :: OSI Approved :: GNU Lesser General Public License v2' +
          ' or later (LGPLv2+)',
          'Operating System :: POSIX',
          'Programming Language :: Python',
          'Programming Language :: Python :: 3.6',
          'Topic :: Software Development',
          'Topic :: Software Development :: Libraries :: Python Modules',
          'Topic :: Software Development :: Quality Assurance',
          'Topic :: Software Development :: Testing',
      ])
