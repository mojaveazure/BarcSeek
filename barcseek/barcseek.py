#!/usr/bin/env python3

"""Parition a FASTQ file (or paired FASTQ files) based on barcodes"""

import sys
if not (sys.version_info.major == 3 and sys.version_info.minor >= 5):
    sys.exit("Please use Python 3.5 or higher")


#   Load standard modules
import os
import time
import signal
import logging
import warnings
from multiprocessing import Lock
from multiprocessing.pool import Pool

#   Load custom modules
import barcseek.barcodes as barcodes
import barcseek.utilities as utilities
import barcseek.arguments as arguments

LOCK = Lock()

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
    args = vars(parser.parse_args()) # type: Dict[str, Any]
    #   Make an output directory
    # if os.path.exists(args['outdirectory']):
    #     args['outdirectory'] = args['outdirectory'] + time.strftime('_%Y-%m-%d_%H:%M')
    os.makedirs(args['outdirectory'], exist_ok=True)
    #   Make a prefix for project-level output files
    output_prefix = os.path.join(args['outdirectory'], sys.argv[0]) # type: str
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
    #   Read in the sample sheet and match barcode sequences to each sample
    sample_sheet = utilities.load_sample_sheet(sheet_file=args['sample_sheet']) # type: Dict[str, Tuple[str, Optional[str]]]
    sample_barcodes = utilities.match_barcodes(sample_sheet=sample_sheet, barcodes_dictionary=barcodes_dict) # type: Dict[str, Tuple[str, Optional[str]]]
    print(sample_barcodes)
    raise SystemExit
    #   Create the multiprocessing pool
    #   Tell the pool to ignore SIGINT (^C)
    #   by turning INTERUPT signals into IGNORED signals
    sigint_handler = signal.signal(signal.SIGINT, signal.SIG_IGN) # type: function
    #   Setup our multiprocessing pool
    #   Allow the user to specify the number of jobs to run at once
    #   If not specified, let multiprocessing figure it out
    if args['num_cores']:
        pool = Pool(processes=args['num_cores'])
    else:
        pool = Pool()
    #   Re-enable the capturing of SIGINT, catch with KeyboardInterrupt
    #   or ExitPool, depending on how the exit was initiated
    #   Note: SystemExits are swallowed by Pool, no way to change that
    signal.signal(signal.SIGINT, sigint_handler)
    if getattr(pool, '_processes') > 1:
        try:
            #   Use map_async and get with a large timeout
            #   to allow for KeyboardInterrupts to be caught
            #   and handled with the try/except
            pass
        except KeyboardInterrupt:
            pool.terminate()
            pool.join()
            raise SystemExit('\nkilled')
        else:
            pool.join()
    #   Otherwise, don't bother with pool.map() make life easy
    else:
        #   Clean up the pool
        pool.close(); pool.terminate(); pool.join()
        #   Use standard map
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
