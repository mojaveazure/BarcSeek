#!/usr/bin/env python3

"""Argument utilties for BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


#   Load standard modules
import argparse
import multiprocessing

_HELP_WRAP = 60 # type: int
_ERROR_DEFAULT = 1 # type: int
_OUTDIR_DEFAULT = 'output' # type: str
_VERBOSITY_DEFAULT = 'info' # type: str
_VERBOSITY_LEVELS = ( # type: Tuple[str]
    'debug',
    'info',
    'warning',
    'error',
    'critical'
)

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
        formatter_class=argparse.RawDescriptionHelpFormatter,
        add_help=False
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
        help="Set the verbosity level, choose from '%s'; defaults to '%s'" % ("', '".join(_VERBOSITY_LEVELS), _VERBOSITY_DEFAULT)
    )
    parser.add_argument( # Number of cores
        '--parallel',
        dest='num_cores',
        type=_num_cores,
        const=None,
        default=1,
        nargs='?',
        required=False,
        metavar='num jobs',
        help="Run %(prog)s in parallel; if passed, can optionally specify the number of jobs to run at once"
    )
    parser.add_argument( # Output directory
        '-o',
        '--output-directory',
        dest='outdirectory',
        type=str,
        default=_OUTDIR_DEFAULT,
        required=False,
        metavar='output directory',
        help="Choose where all output files are to be stored; defaults to '%s'" % _OUTDIR_DEFAULT
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
        required=True,
        metavar='FORWARD FASTQ',
        help="Provide a filepath for the forward/single FASTQ file"
    )
    inputs.add_argument( # Reverse FASTQ
        '-r',
        '--reverse-fastq',
        dest='reverse',
        type=str,
        default=None,
        required=False,
        metavar='REVERSE FASTQ',
        help="Provide a filepath for the optional reverse FASTQ file"
    )
    inputs.add_argument( # Sample sheet
        '-s',
        '--sample-sheet',
        dest='sample_sheet',
        type=str,
        default=None,
        required=True,
        metavar='SAMPLE SHEET',
        help="Provide a filepath for the sample sheet"
    )
    inputs.add_argument( # Barcodes file
        '-b',
        '--barcodes',
        dest='barcodes',
        type=str,
        required=True,
        default=None,
        metavar='BARCODES',
        help="Provide a filepath for the barcodes CSV file"
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
        required=False,
        metavar='ERROR',
        help="This is how many mismatches in the barcode we allowed before rejecting, defaults to %s" % _ERROR_DEFAULT
    )
    return parser
