#!/usr/bin/env python3

"""Utilities for dealing with barcodes"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher for this module: " + __name__)


#   Import standard modules
# import json
import time
import logging
from typing import Dict, Tuple
from collections import Counter

#   Import custom modules
import barcseek.utilities as utilities
from barcseek.partition import IUPAC_CODES

#   Import installed modules
try:
    import regex
except ImportError as error:
    sys.exit("Please install " + error.name)


def expand_iupac(barcode: str) -> Tuple[str]:
    """Expand IUPAC codes, i.e. turn 'AY' to ['AC', 'AT'], removes 'N's"""
    barcode = barcode.upper()
    if all((i in 'ACGTN' for i in set(barcode))):
        return (barcode.replace('N', ''),)
    pos = regex.search(r'[%s]' % ''.join(IUPAC_CODES.keys()), barcode).start()
    code = barcode[pos]
    return utilities.unpack(collection=(expand_iupac(barcode.replace(code, i, 1)) for i in IUPAC_CODES[code]))


def read_barcodes(barcodes_file: str) -> Dict[str, str]:
    """Read the barcodes CSV"""
    logging.info("Reading in barcodes file %s", barcodes_file)
    read_start = time.time() # type: float
    barcodes_dict = dict()
    try:
        with open(barcodes_file, 'r') as bfile:
            for line in bfile: # type: str
                if line.startswith('#'):
                    continue
                line = line.strip().split(',')
                if len(line) == 2:
                    barcodes_dict[line[0]] = line[1]
    except FileNotFoundError:
        raise SystemExit(logging.critical("Cannot find barcodes file %s", barcodes_file))
    if not barcodes_dict:
        raise ValueError(logging.error("No barcodes found in the barcodes file"))
    logging.debug("Reading in barcodes took %s seconds", round(time.time() - read_start, 3))
    return barcodes_dict


def barcode_check(barcode_dict: Dict[str, str]) -> bool:
    """Checks whether or not there are barcodes in use that are ambiguous and could thus recognize the same sequence.
    For example the barcodes 'AY' and 'AW' both recognize 'AT'.
    Does not check for ambiguity with regards to UMIs, i.e. strings of 'N'. So 'ACGN' and 'ACGT' are recognized as different
    even though they can both match 'ACGT'."""
    logging.info("Checking for ambiguous and duplicate barcodes")
    check_start = time.time() # type: float
    barcodes = utilities.unpack(collection=barcode_dict.values()) # type: Iterable[str]
    expanded_barcodes = utilities.unpack(expand_iupac(bc) for bc in barcodes) # type: Tuple[str]
    multiplicate_barcodes = dict(filter(lambda item: item[1] > 1 , Counter(expanded_barcodes).items())) # type: Dict[str, int]
    logging.debug("Checking barcode validity took %s seconds", round(time.time() - check_start, 3))
    return bool(multiplicate_barcodes)


# def extract_barcodes(sample_sheet, barcode_csv):
#     """Returns a dictionary, Keys are the sample_names, values are the barcodes."""
#     with open(sample_sheet) as ss_reader, open(barcode_csv) as barcode_reader:
#         ss_file = itertools.islice(csv.reader(ss_reader, delimiter='\t'), 1, None)
#         barcode_file = csv.reader(barcode_reader, delimiter=',')
#         csv_dict = {int(line[0]):line[1] for line in barcode_file}
#         ss_dict = defaultdict(list)
#         for line in ss_file:
#             barcode1, barcode2, samplename = line[0], line[1], line[2]
#             if barcode1:
#                 ss_dict[samplename].append(csv_dict[int(barcode1)])
#             if barcode2:
#                 ss_dict[samplename].append(csv_dict[int(barcode2)])
#         filtered_barcodes = list(filter(lambda sample: not(sample[1]), ss_dict.items()))
#         if filtered_barcodes:
#             raise InputError('One of your samples in your sample_sheet.tab has no barcodes associated with itself.')
#         return ss_dict
