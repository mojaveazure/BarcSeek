#!/usr/bin/env python3

"""Utilities for BarcSeek"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


import os
import gzip
# from collections import namedtuple
from typing import Iterable, Tuple, Any

from barcseek import fastq

try:
    from Bio.SeqIO.QualityIO import FastqGeneralIterator
except ImportError as error:
    sys.exit("Please install " + error.name)


# Read = namedtuple('Read', ('name', 'seq', 'qual'))

def unpack(collection: Iterable[Any]) -> Tuple[Any]:
    """Unpack a series of nested lists, sets, or tuples"""
    result = [] # type: List
    for item in collection: # type: Any
        if hasattr(item, '__iter__') and not isinstance(item, str):
            result.extend(unpack(collection=item))
        else:
            result.append(item)
    return tuple(result)


def load_fastq(fastq_file: str) -> Tuple[fastq.Read]:
    """Load a FASTQ file"""
    # logging.info("Reading in FASTQ file '%s'...", fastq_file)
    # read_start = time.time() # type: float
    reads = [] # type: List[Read]
    if os.path.splitext(fastq_file)[-1] == '.gz':
        my_open = gzip.open # type: function
    else:
        my_open = open # type: function
    with my_open(fastq_file, 'rt') as ffile:
        for read in FastqGeneralIterator(ffile): # type: Tuple[str, str, str]
            name, seq, qual = read # type: str, str, str
            # reads.append(Read(name=name, seq=seq, qual=qual))
            reads.append(fastq.Read(read_id=name, seq=seq, qual=qual))
    # logging.debug("Reading in FASTQ file '%s' took %s seconds", fastq_file, round(time.time() - read_start, 3))
    return tuple(reads)
