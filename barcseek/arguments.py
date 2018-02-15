#!/usr/bin/env python3

"""Argument utilties for BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


import argparse
import textwrap
import multiprocessing

_HELP_WRAP = 60 # type: int
_ERROR_DEFAULT = 1 # type: int
_VERBOSITY_DEFAULT = 'info' # type: str
_VERBOSITY_LEVELS = (
    'debug',
    'info',
    'warning',
    'error',
    'critical'
)

def _help_text(text: str, wrap: int=45) -> str:
    return '\n'.join(textwrap.wrap(text, wrap))

def _num_cores(value: str) -> int:
    try:
        value = int(value) # type: int
    except ValueError:
        raise argparse.ArgumentTypeError("Must pass an integer value")
    try:
        assert value < multiprocessing.cpu_count()
    except AssertionError:
        raise argparse.ArgumentTypeError("Cannot have more jobs (%s) than cores available (%s)" % (value, multiprocessing.cpu_count()))
    except NotImplementedError:
        pass
    return value


def set_args() -> argparse.ArgumentParser:
    """Make an argument parser"""
    parser = argparse.ArgumentParser( # type: argparse.ArgumentParser
        description=r'''
                     -----------------------------------
                    < Pull DNA barcodes from FASTQ files >
                     -----------------------------------
                     /
     \ ______/ V`-, /
      }        /~~
     /_)^ --,r'
    |b      |b
     ''',
        formatter_class=argparse.RawTextHelpFormatter,
        add_help=True
    )
    #   Arguments for verbosity and logging
    parser.add_argument( # Verbosity
        '-v',
        '--verbosity',
        dest='verbosity',
        type=str.lower,
        choices=_VERBOSITY_LEVELS,
        default=_VERBOSITY_DEFAULT,
        required=False,
        metavar='verbosity',
        help=_help_text(text="Set the verbosity level, choose from '%s'; defaults to '%s'" % ("', '".join(_VERBOSITY_LEVELS), _VERBOSITY_DEFAULT))
    )
    parser.add_argument( # Log file
        '-l',
        '--logfile',
        dest='logfile',
        type=str,
        default=None,
        required=False,
        metavar='log file',
        # help=_help_text(text="Specify a file for the log messages, defaults to stderr")
        help=argparse.SUPPRESS
    )
    #   Input arguments
    inputs = parser.add_argument_group(
        title='input arguments',
        description='Provide inputs for %(prog)s'
    )
    inputs.add_argument( # Forward FASTQ
        '-f',
        '--forward-fastq',
        dest='forward',
        type=str,
        default=None,
        metavar='FORWARD FASTQ',
        help=_help_text(text="Provide a filepath for the forward FASTQ file"),
        required=True
    )
    inputs.add_argument( # Reverse FASTQ
        '-r',
        '--reverse-fastq',
        dest='reverse',
        type=str,
        default=None,
        metavar='REVERSE FASTQ',
        help=_help_text(text="Provide a filepath for the reverse FASTQ file")
    )
    inputs.add_argument( # Sample sheet
        '-s',
        '--sample-sheet',
        dest='sample_sheet',
        type=str,
        default=None,
        metavar='SAMPLE SHEET',
        help=_help_text(text="Provide a filepath for the sample sheet"),
        required=True
    )
    inputs.add_argument( # Barcodes file
        '-b',
        '--barcodes',
        dest='barcodes',
        type=str,
        default=None,
        metavar='BARCODES',
        help=_help_text(text="Provide a filepath for the barcodes CSV file"),
        required=True
    )
    barcodes = parser.add_argument_group(
        title='barcode options',
        description="Set parameters for barcode demultiplexing"
    )
    barcodes.add_argument( # Number of errors allowed
        '-e',
        '--error',
        dest='error',
        type=int,
        default=_ERROR_DEFAULT,
        metavar='ERROR',
        help=_help_text(text="This is how many mismatches in the barcode we allowed before rejecting, defaults to %s" % _ERROR_DEFAULT)
    )
    # parser.add_argument( # Numlines?
    #     '-l',
    #     '--numlines',
    #     dest='numlines',
    #     type=int,
    #     default=40000,
    #     metavar='NUMLINES',
    #     help='We internally split your input file(s) into \nmany smaller files, after -l lines.\n[OPTIONAL, DEFAULT=40000]'
    # )
    return parser
