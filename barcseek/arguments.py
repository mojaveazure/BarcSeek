#!/usr/bin/env python3

"""Argument utilties for BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


import argparse

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
    parser.add_argument( # Forward FASTQ
        '-f',
        '--forward-fastq',
        dest='forward',
        type=str,
        default=None,
        metavar='FORWARD FASTQ',
        help="Provide a filepath for the Forward FASTQ file.\n[REQUIRED]",
        required=True
    )
    parser.add_argument( # Reverse FASTQ
        '-r',
        '--reverse-fastq',
        dest='reverse',
        type=str,
        default=None,
        metavar='REVERSE FASTQ',
        help="Provide a filepath for the Reverse FASTQ file.\n[OPTIONAL]"
    )
    parser.add_argument( # Sample sheet
        '-s',
        '--sample-sheet',
        dest='sample',
        type=str,
        default=None,
        metavar='SAMPLE SHEET',
        help="Provide a filepath for the Sample Sheet file.\n[REQUIRED]",
        required=True
    )
    parser.add_argument( # Barcodes file
        '-b',
        '--barcodes',
        dest='barcodes',
        type=str,
        default=None,
        metavar='BARCODES',
        help="Provide a filepath for the Barcodes CSV file.\n[REQUIRED]",
        required=True
    )
    parser.add_argument( # Number of errors allowed
        '-e',
        '--error',
        dest='error',
        type=int,
        default=1,
        metavar='ERROR',
        help="This is how many mismatches in the barcode \nwe allowed before rejecting.\n[OPTIONAL, DEFAULT=1]"
    )
    parser.add_argument( # Numlines?
        '-l',
        '--numlines',
        dest='numlines',
        type=int,
        default=40000,
        metavar='NUMLINES',
        help='We internally split your input file(s) into \nmany smaller files, after -l lines.\n[OPTIONAL, DEFAULT=40000]'
    )
    return parser
