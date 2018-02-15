#!/usr/bin/env python3

"""Setup BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher")


from setuptools import setup
from setuptools.command.install import install

# Some basic information
NAME = 'BarcSeek'
URL = 'https://github.com/mojaveazure/BarcSeek'

#   Platforms
PLATFORMS = ['Linux', 'Mac OS-X', 'UNIX']

#   Classifiers
CLASSIFIERS = [
    #   See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    #   For more classfiiers
    #   How mature is this project? Common values are
    'Development Status :: 5 - Production/Stable',
    #   What environment does this run in?
    'Environment :: Console',
    #   Indicate who your project is intended for
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    #   Language
    'Natural Language :: English',
    #   Pick your license as you wish (should match "license" above)
    'License :: OSI Approved :: MIT License',
    #   Specify the Python versions you support here. In particular, ensure
    #   that you indicate whether you support Python 2, Python 3 or both.
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    #   Operating systems we support
    # 'Operating System :: Microsoft :: Windows',
    'Operating System :: MacOS :: MacOS X',
    'Operating System :: POSIX :: Linux',
    'Operating System :: Unix',
]

#   Specify Python version
PYTHON_REQUIRES = '>=3.5'

#   Dependencies
INSTALL_REQUIRES = [
    'regex',
    'biopython'
]

#   Packages
PACKAGE_DIR = 'barcseek'
PACKAGES = [
    PACKAGE_DIR
]

#   Entry points into the program
ENTRY_POINTS = {
    'console_scripts': [
        '%(name)s = %(package)s.%(package)s:main' % {'name': NAME, 'package': PACKAGE_DIR}
    ]
}

#   Commands available for setup.py
CMD_CLASS = {
    'install': install
}

#   Run setup
setup(
    name=NAME.lower(),
    url=URL,
    platforms=PLATFORMS,
    python_requires=PYTHON_REQUIRES,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    cmdclass=CMD_CLASS
)
