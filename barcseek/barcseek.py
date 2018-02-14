#!/usr/bin/env python3

"""Parition a FASTQ file (or paired FASTQ files) based on barcodes"""

import sys
if sys.version_info.major is not 3 and sys.version_info.minor < 5:
    sys.exit("Please use Python 3.5 or higher")


import csv
import json
import argparse
from itertools import chain, islice
from collections import Counter, defaultdict

try:
    import regex
except ImportError as error:
    sys.exit("Please install " + error.name)


try:
    # from parallel import parallelize
    from partition import IUPAC_CODES
except ImportError:
    sys.exit("Please leave this program in its directory to load custom modules")


class InputError(Exception):
    '''An error occurred because of your input'''
    def __init__(self, message):
        super().__init__(self)
        self.message = message


#   A function to create an argument parser
def _set_args():
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
    parser.add_argument(
        '-f',
        '--forward-fastq',
        dest='forward',
        type=str,
        default=None,
        metavar='FORWARD FASTQ',
        help="Provide a filepath for the Forward FASTQ file.\n[REQUIRED]",
        required=True
    )
    parser.add_argument(
        '-r',
        '--reverse-fastq',
        dest='reverse',
        type=str,
        default=None,
        metavar='REVERSE FASTQ',
        help="Provide a filepath for the Reverse FASTQ file.\n[OPTIONAL]"
    )
    parser.add_argument(
        '-s',
        '--sample-sheet',
        dest='sample',
        type=str,
        default=None,
        metavar='SAMPLE SHEET',
        help="Provide a filepath for the Sample Sheet file.\n[REQUIRED]",
        required=True
    )
    parser.add_argument(
        '-b',
        '--barcodes',
        dest='barcodes',
        type=str,
        default=None,
        metavar='BARCODES',
        help="Provide a filepath for the Barcodes CSV file.\n[REQUIRED]",
        required=True
    )
    parser.add_argument(
        '-e',
        '--error',
        dest='error',
        type=int,
        default=1,
        metavar='ERROR',
        help="This is how many mismatches in the barcode \nwe allowed before rejecting.\n[OPTIONAL, DEFAULT=1]"
    )
    parser.add_argument(
        '-l',
        '--numlines',
        dest='numlines',
        type=int,
        default=40000,
        metavar='NUMLINES',
        help='We internally split your input file(s) into \nmany smaller files, after -l lines.\n[OPTIONAL, DEFAULT=40000]'
    )
    
    return parser


def expand_iupac(barcode):
    '''
    Expand IUPAC codes, i.e. turn 'AY' to ['AC', 'AT'], removes 'N's
    '''
    barcode = barcode.upper()
    if all((i in 'ACGTN' for i in set(barcode))):
        return barcode.replace('N','')
    else:
        pos = regex.search(r'[%s]' % ''.join(IUPAC_CODES.keys()), barcode).start()
        code = barcode[pos]
        return (expand_iupac(barcode.replace(code, i, 1)) for i in IUPAC_CODES[code])


def unpack(collection):
    '''
    Unpack a series of nested lists, sets, or tuples
    '''
    result = [] # type: List
    for item in collection:
        # if isinstance(item, (list, set, tuple)):
        if hasattr(item, '__iter__') and not isinstance(item, str):
            result.extend(unpack(collection=item))
        else:
            result.append(item)
    return result


def barcode_check(barcode_dict):
    '''
    Checks whether or not there are barcodes in use that are ambiguous and could thus recognize the same sequence.
    For example the barcodes 'AY' and 'AW' both recognize 'AT'.
    Does not check for ambiguity with regards to UMIs, i.e. strings of 'N'. So 'ACGN' and 'ACGT' are recognized as different
    even though they can both match 'ACGT'.
    '''
    barcodes = chain.from_iterable(barcode_dict.values())
    expanded_barcodes = unpack(expand_iupac(bc) for bc in barcodes)
    multiplicate_barcodes = dict(filter(lambda item: item[1] > 1 , Counter(expanded_barcodes).items()))
    return multiplicate_barcodes


def extract_barcodes(sample_sheet, barcode_csv):
    '''
    Returns a dictionary, Keys are the sample_names, values are the barcodes.
    '''

    with open(sample_sheet) as ss_reader, open(barcode_csv) as barcode_reader:
        ss_file = islice(csv.reader(ss_reader, delimiter='\t'),1,None)
        barcode_file = csv.reader(barcode_reader, delimiter=',')
        csv_dict = {int(line[0]):line[1] for line in barcode_file}

        ss_dict = defaultdict(list)
        for line in ss_file:
            barcode1, barcode2, samplename = line[0], line[1], line[2]
            if barcode1:
                ss_dict[samplename].append(csv_dict[int(barcode1)])
            if barcode2:
                ss_dict[samplename].append(csv_dict[int(barcode2)])
        filtered_barcodes = list(filter(lambda sample: not(sample[1]), ss_dict.items()))
        if filtered_barcodes:
            raise InputError('One of your samples in your sample_sheet.tab has no barcodes associated with itself.')
        return ss_dict



def main(args):
    from parallel import parallelize
    '''Run the program'''
    if args['numlines']%4 != 0:
        raise InputError('-l  must be divisible by four'+str(args['numlines']))
    sample_dict = extract_barcodes(args['sample'],args['barcodes'])
    barcode_ambiguity_dict = barcode_check(sample_dict)
    if barcode_ambiguity_dict:
        raise InputError("There are ambiguous barcodes \n" + str(json.dumps(barcode_ambiguity_dict, indent=2)))
    #call the parallel layer which does the work:
    '''def parallelize(barcodes:tuple, samples:dict, num_chunks:int, forward_fastq:str,
                reverse_fastq:Optional(str) = None)'''
    parallelize(sample_dict, args['forward'], args['num_lines'], reverse_fastq = args['reverse'])


if __name__ == '__main__':
    PARSER = _set_args() # type: argparse.ArgumentParser
    if not sys.argv[1:]:
        sys.exit(PARSER.print_help())
    ARGS = vars(PARSER.parse_args()) # type: Dict[str, Any]
    main(ARGS)
