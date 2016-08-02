# Let's get some libraries
import configparser
import logging
import handlers
import datapoint
from time import strftime
import os
import sys
from escpos import *

def main():

    # Let's make logging work. Formatting the log here
    logFormatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s","%m/%d/%Y %I:%M:%S %p")
    rootLogger = logging.getLogger()
    
    # Output the log to a file
    fileHandler = logging.FileHandler("dashday.log")
    fileHandler.setFormatter(logFormatter)
    rootLogger.addHandler(fileHandler)
    rootLogger.setLevel(logging.INFO) # Output info to the log by default

    # And output it to the console too
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.WARNING) # Only output warnings to stdout
    rootLogger.addHandler(consoleHandler)

    # Wahey
    logging.info('Dashday process started')

    # Create a new configuration file instance
    configfile = configparser.ConfigParser()

    # Does the user even have a configuration file?
    if os.path.isfile('dashday.cfg') != True:
        # Check for test mode specified in the environment variables
        if "DASHDAY_TESTMODE" in os.environ and os.environ['DASHDAY_TESTMODE'] == '1':
            try:
                maincfg = {'HelloMyNameIs' : "TestModeUsr"}
                datapointcfg = {'TextRegionCode': '514', 'ForecastLocation': '3672', 'DataPointKey': os.environ['DASHDAY_DPKEY']}
                debugcfg = {'TestMode': "1", 'LogLevel': "DEBUG"}
            except KeyError:
                handlers.criterr("Incorrectly set test environment variables. Please set up Dashday correctly for testing.")
            logging.warning("Running in environment variable based test mode.")
        else:
            handlers.criterr('dashday.cfg not found. Add dashday.cfg to your directory to continue.')
            # Put onboarding stuff here at some point
    else:
        configfile.read('dashday.cfg')
        datapointcfg = configfile['Weather']
        maincfg = configfile['General']
        debugcfg = configfile['Debug']

    # And let's start the logging!
    numeric_level = getattr(logging, debugcfg['LogLevel'].upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % loglevel)
    rootLogger.setLevel(numeric_level)

    # Connects to the printer (unless test mode is enabled, in which case starts a dummy instance)
    if debugcfg['TestMode'] == "1":
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
    logging.debug("Set the header printing style")
    p.text("Hello,\n" + maincfg['HelloMyNameIs'] + '\n\n')
    logging.debug("Printed the header")
    
    # Time to reset the font
    p.set("LEFT", "A", "normal", 1, 1)
    logging.debug("Unset the header printing style")
    
    # Now let's fetch the more localized and up-to-date but raw data - with an accurate 'real' OS path?
    p.image(os.path.join(os.path.realpath('resources/images/weather') + os.path.sep + wtypes[datapoint.fetchFrcWthrType(datapointcfg['ForecastLocation'],datapointcfg['DataPointKey'])]))
    logging.debug("Printed the localized weather data image")

    # And now we can find the text forecast from the Met Office's DataPoint API
    p.text(datapoint.fetchRegionFrcAsText(datapointcfg['TextRegionCode'],datapointcfg['DataPointKey']))
    logging.debug("Printed the regional weather text")
    
    # Cut the paper! Magic!
    p.cut()
    logging.debug("Printed the localized weather data image")

    # If we're in test mode, print the results to the screen
    if debugcfg['TestMode']:
        print(str(p.output))
        logging.debug("Printed dummy output to stdout")
       
    # Call the "wahey I'm done!" handler
    handlers.closed()

try:
    main()
except (KeyboardInterrupt, SystemExit, EOFError) as e:
    handlers.closed()
    raise
