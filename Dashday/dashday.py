# Let's get some libraries
import configparser
import logging
import handlers
import datapoint
from time import strftime
import os.path
from escpos import *

def main():

    # Create a new configuration file instance
    configfile = configparser.ConfigParser()

    # Does the user even have a configuration file?
    if os.path.isfile('dashday.cfg') != True:
        handlers.criterr('dashday.cfg not found. Add dashday.cfg to your directory to continue.')
        # Put onboarding stuff here at some point

    configfile.read('dashday.cfg')
    datapointcfg = configfile['Weather']
    maincfg = configfile['General']
    debugcfg = configfile['Debug']

    # And let's start the logging!
    numeric_level = getattr(logging, debugcfg['LogLevel'].upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',filename='dashday.log',level=numeric_level)
    logging.info('Dashday process started')

    # Connects to the printer (unless test mode is enabled, in which case starts a dummy instance)
    if debugcfg['testmode']:
        logging.warning('Dashday is in test mode. Nothing will actually be printed - you\'ll just see the output to the printer on the screen.')
        p = printer.Dummy()
    else:
        p = printer.Usb(maincfg['Vendor'],maincfg['Product'])

    # Now we can set up the different weather types and their respective filenames for the image to print
    wtypes = {'NA' : 'questionmark.png',
           '1' : 'sunny.png',
           '3' : 'ptlycloudy.png',
           '5' : 'mist.png',
           '6' : 'fog.png',
           '7' : 'cloudy.png',
           '8' : 'overcast.png',
           '11' : 'drizzle.png',
           '12' : 'lightrain.png',
           '15' : 'heavyrain.png',
           '18' : 'sleet.png',
           '21' : 'hail.png',
           '24' : 'lightsnow.png',
           '27' : 'heavysnow.png',
           '30' : 'thunder.png',
    }


    # Setup the printer for the beautiful header, and then print it
    p.set("LEFT", "B", "B", 2, 2)
    p.text("Hello,\n" + maincfg['HelloMyNameIs'] + '\n\n')
    
    # Time to reset the font
    p.set("LEFT", "A", "normal", 1, 1)
    
    # Now let's fetch the more localized and up-to-date but raw data 
    p.image('resources\\images\\weather\\' + wtypes[datapoint.fetchFrcWthrType(datapointcfg['ForecastLocation'],datapointcfg['DataPointKey'])])

    # And now we can find the text forecast from the Met Office's DataPoint API
    p.text(datapoint.fetchRegionFrcAsText(datapointcfg['TextRegionCode'],datapointcfg['DataPointKey']))
    
    # Cut the paper! Magic!
    p.cut()

    # If we're in test mode, print the results to the screen
    if debugcfg['testmode']:
        print(str(p.output))
       
    # Call the "wahey I'm done!" handler
    handlers.closed()

try:
    main()
except (KeyboardInterrupt, SystemExit, EOFError) as e:
    handlers.closed()
    raise
