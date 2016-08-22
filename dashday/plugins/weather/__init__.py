name = "Weather"
description = "Prints the weather and all sorts of associated stuff. Gets the data from the Met Office API."
version = "v1.1"
author = "mashedkeyboard"

# Configuration settings for the web interface
hasconfig = True
configfile = "config/weather.cfg"
configopts = {'Info': {'TextRegionCode': 'Region code',
                       'ForecastLocation': 'Forecast location code',
                       'DataPointKey': 'DataPoint API key'}}