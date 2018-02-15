#!/usr/bin/env python3

"""Parition a FASTQ file (or paired FASTQ files) based on barcodes"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher")


#   Load standard modules
import os
import time
import logging
import warnings

#   Load custom modules
import barcseek.barcodes as barcodes
import barcseek.utilities as utilities
import barcseek.arguments as arguments

def _set_verbosity(level): # type: (str) -> int
    level = level.upper()
    if level == 'DEBUG':
        log_level = logging.DEBUG # type: int
    elif level == 'INFO':
        log_level = logging.INFO # type: int
    elif level == 'WARNING':
        log_level = logging.WARNING # type: int
    elif level == 'ERROR':
        log_level = logging.ERROR # type: int
    elif level == 'CRITICAL':
        log_level = logging.CRITICAL # type: int
    else:
        raise ValueError("'level' must be one of 'DEBUG', 'INFO', 'WARNING', 'ERROR', or 'CRITICAL'")
    return log_level


def barcseek() -> None:
    """Run BarcSeek"""
    pass


def main() -> None:
    """Run BarcSeek"""
    parser = arguments.set_args() # type: argparse.ArgumentParser
    if not sys.argv[1:]:
        sys.exit(parser.print_help())
    args = {key: value for key, value in vars(parser.parse_args()).items() if value is not None} # type: Dict[str, Any]
    # #   Make an output directory
    # if os.path.exists(args['outdirectory']):
    #     args['outdirectory'] = args['outdirectory'] + time.strftime('_%Y-%m-%d_%H:%M')
    # try:
    #     os.makedirs(args['outdirectory'])
    # except OSError:
    #     pass
    # finally:
    #     #   Make a prefix for project-level output files
    #     output_prefix = os.path.join(args['outdirectory'], args['project']) # type: str
    output_prefix = os.path.join(os.getcwd(), 'BarcSeek') # type: str
    #   Setup the logger
    #   Formatting values
    log_format = '%(asctime)s %(levelname)s:\t%(message)s' # type: str
    date_format = '%Y-%m-%d %H:%M:%S' # type: str
    #   Formatters
    stripped_formatter = utilities.StrippedFormatter(fmt=log_format, datefmt=date_format) # utilities.StrippedFormatter
    colored_formater = utilities.ColoredFormatter(fmt=log_format, datefmt=date_format) # type: utilities.ColoredFormatter
    #   Open /dev/null (or whatever it is on Windows) to send basic stream information to
    devnull = open(os.devnull, 'w')
    #   Configure the logger
    verbosity = _set_verbosity(level=args['verbosity']) # type: int
    logging.basicConfig(
        stream=devnull,
        level=verbosity,
    )
    #   If we're being verbose, capture other warnings (mainly matplotlib and numpy)
    #   Otherwise, ignore them
    if verbosity == logging.DEBUG:
        logging.captureWarnings(True)
    else:
        warnings.filterwarnings('ignore')
    #   Setup a FileHandler for the log file
    #   Use a StrippedFormatter to remove extra ANSI color codes
    logname = output_prefix + '.log'
    logfile = logging.FileHandler(filename=logname, mode='w') # type: Logging.FileHandler
    logfile.setFormatter(stripped_formatter)
    logging.getLogger().addHandler(logfile)
    #   Setup the console handler
    #   Use a ColoredFormatter because colors are cool
    console = logging.StreamHandler() # type: logging.StreamHandler
    console.setFormatter(colored_formater)
    logging.getLogger().addHandler(console)
    #   Begin the program
    logging.info("Welcome to %s!", os.path.basename(sys.argv[0]))
    program_start = time.time() # type: float
    #   Read in the barcodes
    barcodes_dict = barcodes.read_barcodes(barcodes_file=args['barcodes']) # type: Dict[str, str]
    if barcodes.barcode_check(barcode_dict=barcodes_dict):
        raise ValueError(logging.error("Cannot have ambiguous or duplicate barcodes"))
    #   End the program
    logging.debug("Entire program took %s seconds to run", round(time.time() - program_start, 3))
    devnull.close()
    try:
        logfile.close()
    except NameError:
        pass
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
