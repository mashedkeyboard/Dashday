## PLUGIN NAME: weather
## PLUGIN AUTHOR: mashedkeyboard
## PLUGIN DESCRIPTION: Prints an icon and weather text report to the dashday printout based on the Met Office's DataPoint
## PLUGIN CONFIGURATION FILES: weather.cfg

import os
import handlers
import configparser
import pluginloader
from plugins.weather import datapoint

def init():
    global config
    global wtypes
    global weathercfg

    # Load configuration and all that jazz
    config = configparser.ConfigParser()
    if os.path.isfile('config/weather.cfg'):
        config.read('config/weather.cfg')
        weathercfg = config['Info']
    else:
        if "DASHDAY_TESTMODE" in os.environ and os.environ['DASHDAY_TESTMODE'] == '1':
            try:
                weathercfg = {'TextRegionCode': '514', 'ForecastLocation': '3672', 'DataPointKey': os.environ['DASHDAY_DPKEY']}
            except KeyError:
                handlers.criterr("Incorrectly set test environment variables. Please set up Dashday correctly for testing.")
        else:
            handlers.err('Cannot find weather.cfg. weather has not been loaded.')
            pluginloader.unload('weather')

    # Convert the weather types returned from the Met Office API into something vaguely sensible
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
           '30' : 'thunder.png'
    }

def print(p):
    # Now let's fetch the more localized and up-to-date but raw data - with an accurate 'real' OS path?
    p.image(os.path.join(os.path.realpath('resources/images/weather') + os.path.sep + wtypes[datapoint.fetchFrcWthrType(weathercfg['ForecastLocation'],weathercfg['DataPointKey'])]))
    handlers.debug("Weather printed the localized weather data image")

    # And now we can find the text forecast from the Met Office's DataPoint API
    p.text(datapoint.fetchRegionFrcAsText(weathercfg['TextRegionCode'],weathercfg['DataPointKey']))
    handlers.debug("Weather printed the regional weather text")