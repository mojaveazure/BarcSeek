#!/usr/bin/env python3

"""Utilities for BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


#   Load standard modules
import os
import gzip
import time
import logging
from typing import Iterable, Tuple, Dict, Any, Optional

#   Load custom modules
import barcseek.fastq as fastq

#   Load installed modules
try:
    from Bio.SeqIO.QualityIO import FastqGeneralIterator
except ImportError as error:
    sys.exit("Please install " + error.name)


class StrippedFormatter(logging.Formatter):
    """A formatter where all ANSI formatting is removed"""

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record): # type: (logging.LogRecord) -> str
        """Strip ANSI formatting from log messages"""
        message = logging.Formatter.format(self, record) # type: str
        while True:
            #   In Python, '\x1b' == '\033', so both codes for ANSI formatting are covered
            start = message.find('\x1b') # type: int
            #   If no ASI formatting is found break
            if start == -1:
                break
            #   Find the first 'm' after the ANSI code start
            #   and remove everything between and including
            #   the ANSI code start and the 'm'
            m_pos = message.find('m', start) # type: int
            message = message[:start] + message[m_pos + 1:]
        return message


class ColoredFormatter(logging.Formatter):
    """A colorized formatter for logging"""

    _colors = { # type: Dict[int, str]
        50: '\x1b[1m\x1b[31m', # CRITICAL: bold red
        40: '\x1b[31m', # ERROR: red
        30: '\x1b[33m', # WARNING: yellow
        20: '\x1b[32m', # INFO: green
        10: '\x1b[36m' # DEBUG: cyan
    }

    _default = '\x1b[0m' # Anything else: reset

    def __init__(self, *args, **kwargs):
        logging.Formatter.__init__(self, *args, **kwargs)

    def format(self, record): # type: (logging.LogRecord) -> str
        """Colorize log messages"""
        message = logging.Formatter.format(self, record) # type: str
        if sys.platform not in ('win32', 'cygwin'):
            color_level = min(self._colors.keys(), key=lambda level: abs(level - record.levelno)) # type: int
            color_level = min((color_level, record.levelno)) # type: int
            color = self._colors.get(color_level, self._default) # type: str
            message = color + message + self._default # type: str
        return message


def unpack(collection: Iterable[Any]) -> Tuple[Any]:
    """Unpack a series of nested lists, sets, or tuples"""
    result = [] # type: List
    for item in collection: # type: Any
        if hasattr(item, '__iter__') and not isinstance(item, str):
            result.extend(unpack(collection=item))
        else:
            result.append(item)
    return tuple(result)


def load_fastq(fastq_file: str, pair: Optional[str]=None) -> Tuple[fastq.Read]:
    """Load a FASTQ file"""
    logging.info("Reading in FASTQ file %s", fastq_file)
    read_start = time.time() # type: float
    reads = {} # type: Dict[str, fastq.Read]
    if os.path.splitext(fastq_file)[-1] == '.gz':
        my_open = gzip.open # type: function
    else:
        my_open = open # type: function
    with my_open(fastq_file, 'rt') as ffile:
        for read in FastqGeneralIterator(ffile): # type: Tuple[str, str, str]
            name, seq, qual = read # type: str, str, str
            reads[name] = fastq.Read(read_id=name, seq=seq, qual=qual)
    logging.debug("Reading in FASTQ file %s took %s seconds", fastq_file, round(time.time() - read_start, 3))
    if pair:
        logging.info("Reading in reverse FASTQ file %s", pair)
        reverse_start = time.time() # type: float
        if os.path.splitext(pair)[-1] == '.gz':
            my_open = gzip.open # type: function
        else:
            my_open = open # type: function
        with my_open(pair, 'rt') as rfile:
            for rread in FastqGeneralIterator(rfile): # type: Tuple[str, str, str]
                rname, rseq, rqual = rread # type: str, str, str
                try:
                    reads[rname].add_reverse(seq=rseq, qual=rqual)
                except KeyError:
                    logging.error("Reverse read %s doesn't match any reads in the forward FASTQ file", rname)
        logging.debug("Reading in reverse FASTQ file took %s seconds", round(time.time() - reverse_start, 3))
    return tuple(reads.values())


def load_sample_sheet(sheet_file: str) -> Dict[str, Tuple[str, Optional[str]]]:
    """Load in the sample sheet"""
    logging.info("Reading in sample sheet %s", sheet_file)
    sheet_start = time.time() # type: float
    sample_sheet = dict()
    with open(sheet_file, 'r') as sfile:
        for line in sfile:
            if line.startswith('#'):
                continue
            line = line.strip().split()
            sample_sheet[line[0]] = tuple(line[1:])
    logging.debug("Reading in the sample sheet took %s seconds", round(time.time() - sheet_start, 3))
    return sample_sheet


def match_barcodes(sample_sheet: Dict[str, Tuple[str, Optional[str]]], barcodes_dictionary: Dict[str, str]) -> Dict[str, Tuple[str, Optional[str]]]:
    """Create full barcode sequences for each sample in the sample sheet"""
    logging.info("Matching barcodes for %s samples", len(sample_sheet))
    match_start = time.time() # type: float
    bc_lookup = lambda i: barcodes_dictionary.get(i, i) # type: function
    sample_barcodes = dict() # type: Dict[str, Tuple[str, Optional[str]]]
    for sample, barcodes_list in sample_sheet.items(): # type: str, Tuple[str, Optional[str]]
        if len(barcodes_list) > 2:
            raise SystemExit(logging.error("Each sample can have at most two barcodes sets associated with it, sample %s has %s", sample, len(barcodes_list)))
        barcodes_list = map(lambda i: i.split(','), barcodes_list) # type: Iterable[List[str], List[str]]
        barcodes_filled = tuple(','.join(map(bc_lookup, barcodes)) for barcodes in barcodes_list) # type: Tuple[str]
        sample_barcodes[sample] = barcodes_filled
    logging.debug("Matching barcodes took %s seconds", round(time.time() - match_start, 3))
    return sample_barcodes
