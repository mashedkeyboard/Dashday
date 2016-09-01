import logging
from time import strftime

def closed():
    logging.info('Dashday process stopped')

def criterr(errortext):
    logging.critical('A fatal error occured :: ' + errortext)
    exit()

def err(errortext):
    logging.error('An error occured :: ' + errortext)

def warn(errortext):
    logging.warning(errortext)

def inf(errortext):
    logging.info(errortext)

def debug(errortext):
    logging.debug(errortext)