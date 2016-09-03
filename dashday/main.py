# Let's get some libraries
import configparser
import datetime
import logging
import handlers
import pluginloader
from time import strftime
import os
import usb
import sys
from escpos import *

# Get around a weird Python thing
def start():
    try:
        main()
    except (KeyboardInterrupt, SystemExit, EOFError) as e:
        handlers.closed()
        raise

# Get configuration details from the config file
def getCfg():
    global maincfg
    global pluginlist
    global debugcfg

    try:
        configfile.read('config/dashday.cfg')
    except PermissionError:
        handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
    maincfg = configfile['General']
    pluginlist = configfile['Plugins']['toload'].split(',')
    debugcfg = configfile['Debug']

# Main functionality! Woot!
def main():

    global maincfg
    global pluginlist
    global debugcfg
    global configfile

    # Let's make logging work. Formatting the log here
    logFormatter = logging.Formatter("%(asctime)s: %(levelname)s: %(message)s","%m/%d/%Y %I:%M:%S %p")
    rootLogger = logging.getLogger()
    rootLogger.setLevel(logging.NOTSET) # Make sure the root logger doesn't block any potential output to the fileHandler or consoleHandler

    # And output it to the console
    consoleHandler = logging.StreamHandler()
    consoleHandler.setFormatter(logFormatter)
    consoleHandler.setLevel(logging.WARNING) # Only output warnings to stdout
    rootLogger.addHandler(consoleHandler)
    
    # Finally, output the log to a file
    try:
        fileHandler = logging.FileHandler("dashday.log")
        fileHandler.setFormatter(logFormatter)
        fileHandler.setLevel(logging.INFO) # Output info to the log by default
        rootLogger.addHandler(fileHandler)
    except PermissionError:
        handlers.criterr("Permissions error on dashday.log. Please ensure you have write permissions for the directory.")

    # Wahey
    logging.info('Dashday process started')

    # Create a new configuration file instance
    configfile = configparser.ConfigParser()

    # Does the user even have a configuration file?
    if os.path.isfile('config/dashday.cfg') != True:
        # Check for test mode specified in the environment variables
        if "DASHDAY_TESTMODE" in os.environ and os.environ['DASHDAY_TESTMODE'] == '1':
            try:
                maincfg = {'HelloMyNameIs' : "TestModeUsr"}
                pluginlist = ['weather']
                debugcfg = {'TestMode': "1", 'LogLevel': "DEBUG"}
            except KeyError:
                handlers.criterr("Incorrectly set test environment variables. Please set up Dashday correctly for testing.")
            logging.warning("Running in environment variable based test mode.")
        else:
            handlers.criterr('dashday.cfg not found. Please configure dashday before launch.')
    else:
        getCfg()

    # And let's start the logging!
    numeric_level = getattr(logging, debugcfg['LogLevel'].upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: {0!s}'.format(loglevel))
    consoleHandler.setLevel(numeric_level)
    fileHandler.setLevel(numeric_level)

    # Connects to the printer (unless test mode is enabled, in which case starts a dummy instance)
    if debugcfg['TestMode'] == "1":
        logging.warning('Dashday is in test mode. Nothing will actually be printed - you\'ll just see the output to the printer on the screen.')
        p = printer.Dummy()
        logging.debug("Initialized dummy printer")
    else:
        try:
            p = printer.Usb(int(maincfg['Vendor'],16),int(maincfg['Product'],16))
        except (usb.core.NoBackendError,escpos.exceptions.USBNotFoundError) as e:
            logging.debug(e)
            handlers.criterr("Could not initialize printer. Check a printer matching the vendor and product in the config file is actually connected, and relaunch Dashday.")
        logging.debug("Initialized USB printer")


    # Setup the printer for the beautiful header, and then print it
    p.set(align="LEFT",text_type="B",width=2,height=2)
    logging.debug("Set the header printing style")
    p.text("Hello,\n" + maincfg['HelloMyNameIs'] + '\n\n')
    logging.debug("Printed the header")
    
    # Time to reset the font
    p.set("LEFT", "A", "normal", 1, 1)
    logging.debug("Unset the header printing style")
    
    p.text(datetime.datetime.now().strftime("%a %d %b"))
    
    # Load all the plugins in the plugins list in the config file
    for plugin in pluginlist:
        pluginloader.init(plugin)

    # Print all the things
    pluginloader.printAllPlugins(p)
    
    # Cut the paper! Magic!
    p.cut()
    logging.debug("Ended the print and cut the paper")

    # If we're in test mode, print the results to the screen
    if debugcfg['TestMode'] == "1":
        print(str(p.output))
        logging.debug("Printed dummy output to stdout")
        logging.debug("Debug logging enabled, printing to log:") # this would only appear if they did have debug logging enabled so yeah
        logging.debug(str(p.output))
       
    # Call the "wahey I'm done!" handler
    handlers.closed()

if __name__ == '__main__':
    start()
