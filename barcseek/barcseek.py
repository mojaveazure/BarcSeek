#!/usr/bin/env python3

"""Parition a FASTQ file (or paired FASTQ files) based on barcodes"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher")


#   Load standard modules
# import csv
# import json
# import itertools
# from collections import Counter, defaultdict
# from typing import Iterable, Tuple, Any

import barcseek.barcodes as barcodes
import barcseek.arguments as arguments

# try:
#     # from parallel import parallelize
#     from partition import IUPAC_CODES
# except ImportError:
#     sys.exit("Please leave this program in its directory to load custom modules")

# def extract_barcodes(sample_sheet, barcode_csv):
#     """Returns a dictionary, Keys are the sample_names, values are the barcodes."""
#     with open(sample_sheet) as ss_reader, open(barcode_csv) as barcode_reader:
#         ss_file = itertools.islice(csv.reader(ss_reader, delimiter='\t'),1,None)
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


def main() -> None:
    """Run BarcSeek"""
    parser = arguments.set_args() # type: argparse.ArgumentParser
    if not sys.argv[1:]:
        sys.exit(parser.print_help())
    args = vars(parser.parse_args())
    barcodes_dict = barcodes.read_barcodes(barcodes_file=args['barcodes']) # type: Dict[str, str]
    multiple_barcodes = barcodes.barcode_check(barcode_dict=barcodes_dict) # type: Dict[str, int]
    if multiple_barcodes:
        raise ValueError("Cannot have ambiguous or duplicate barcodes")
    # from parallel import parallelize
    # if args['numlines'] %4 != 0:
    #     raise InputError('-l  must be divisible by four'+str(args['numlines']))
    # sample_dict = extract_barcodes(args['sample'],args['barcodes'])
    # barcode_ambiguity_dict = barcode_check(sample_dict)
    # if barcode_ambiguity_dict:
    #     raise InputError("There are ambiguous barcodes \n" + str(json.dumps(barcode_ambiguity_dict, indent=2)))
    # #call the parallel layer which does the work:
    # '''def parallelize(barcodes:tuple, samples:dict, num_chunks:int, forward_fastq:str,
    #             reverse_fastq:Optional(str) = None)'''
    # parallelize(sample_dict, args['forward'], args['num_lines'], reverse_fastq = args['reverse'])


if __name__ == '__main__':
    main()
