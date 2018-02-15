#!/usr/bin/env python3

"""Setup BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher")


import warnings
from setuptools import setup
from setuptools.command.install import install

warnings.filterwarnings('ignore')

# Some basic information
NAME = 'BarcSeek' # type: str
DESCRIPTION = 'A general barcode partitioning tool for demultiplexing genomic sequencing data'
VERSION = '0.1.0' # type: str
AUTHORS = '\n'.join(("Paul Hoffman", "Joseph Kubiak", "Brian Joseph", "James Abraham", "Tobias Schraink")) # type: str
URL = 'https://github.com/mojaveazure/BarcSeek' # type: str
LICENSE = 'MIT' # type: str

#   Platforms
PLATFORMS = ['Linux', 'Mac OS-X', 'UNIX'] # type: List[str]

#   Classifiers
CLASSIFIERS = [ # type: List[str]
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
PYTHON_REQUIRES = '>=3.5' # type: str

#   Dependencies
INSTALL_REQUIRES = [ # type: List[str]
    'regex',
    'biopython'
]

#   Packages
PACKAGE_DIR = 'barcseek'
PACKAGES = [ # type: List[str]
    PACKAGE_DIR
]

#   Entry points into the program
ENTRY_POINTS = { # type: Dict[str, List[str]]
    'console_scripts': [
        '%(name)s = %(package)s.%(package)s:main' % {'name': NAME, 'package': PACKAGE_DIR}
    ]
}

#   Commands available for setup.py
CMD_CLASS = { # type: Dict[str, type]
    'install': install
}

#   Run setup
setup(
    name=NAME.lower(),
    description=DESCRIPTION,
    version=VERSION,
    author=AUTHORS,
    url=URL,
    license=LICENSE,
    platforms=PLATFORMS,
    python_requires=PYTHON_REQUIRES,
    classifiers=CLASSIFIERS,
    install_requires=INSTALL_REQUIRES,
    packages=PACKAGES,
    entry_points=ENTRY_POINTS,
    cmdclass=CMD_CLASS
)
