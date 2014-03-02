# -*- coding: utf-8 -*-
__author__ = 'mackaiver'

#Lets start with a simple commandline tool
import argparse
import os
import sys
from seins.PageParser import DBPageParser, PageContentError
from seins.HtmlFetcher import FetcherException
import requests.exceptions

from colorama import init, Fore, Style
#init colorama so it works on windows as well.
#The autoreset flag keeps me from using RESET on each line I want to color
init(autoreset=True)

import logging
#create a logger for this module
logger = logging.getLogger(__name__)
#the usual formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
# create a handler and make it use the formatter
handler = logging.StreamHandler()
handler.setFormatter(formatter)
# now tell the logger to use the handler
logger.addHandler(handler)
logger.propagate = False


def is_valid_file(parser, arg):
    (folder, t) = os.path.split(arg)
    #logger.debug('given path is:' + os.path.split(arg))

    if not folder == '' and not os.path.exists(folder):
        parser.error("The folder %s does not exist!" % folder)
    else:
        return arg


def parse_args():
    p = argparse.ArgumentParser(description='Lecker data fetching from EFA via the commandline. ',
                                formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    p.add_argument('-d', default='Universität s-Bahnhof, Dortmund', metavar='--departing_station', type=str,
                   help='Name of the departing station')
    p.add_argument('-a', default='Dortmund hbf', metavar='--arrival_station', type=str,
                   help='Name of the arrival station')

    p.add_argument('-o', metavar='--output', type=lambda path: is_valid_file(p, path), help='path to outputfile')
    p.add_argument('-v', action="store_true", help='Show some nice debug and info logging output')

    args = p.parse_args()
    #check for debug logging
    if args.v:
        logging.basicConfig(level=logging.DEBUG)
    else:
        logging.basicConfig(level=logging.WARN)

    return args.o, args.d, args.a


if __name__ == '__main__':

    (output_path, departure, arrival) = parse_args()
    connections = []

    try:
        page = DBPageParser(departure, arrival)
        connections = page.connections
        if output_path:
            with open(output_path, 'wt') as file:
                file.write(page.html)
                logger.info("Output written to " + output_path)

    except PageContentError as e:
        logger.error('Webpage returned an error message: ' + str(e))
    except FetcherException as e:
        logger.error('Fetcher could not get valid response from server: ' + str(e))

    #do some pretty printing
    print('------------ Connections from:' + departure + '  to: ' + arrival)
    for c in connections:
        print(c)
