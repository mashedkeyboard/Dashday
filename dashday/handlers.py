import logging
from time import strftime

def closed():
    logging.info('Dashday process stopped')

def criterr(errortext):
    logging.critical('A fatal error occured :: ' + errortext + '')
    exit()