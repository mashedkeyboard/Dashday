# Bring in the error handlers
import handlers

# Setting up globals
loadedPlugins = {}

# Initialize a plugin and import it
def init(name):
	try:
		loadedPlugins[name] = __import__('plugins.' + name + '.main',fromlist='main') # fromlist stops it from importing as the root module? python is weird
		loadedPlugins[name].init()
	except Exception as e:
		handlers.err("loading plugin " + name + " :: Exception raised :: " + str(e))

# Get rid of a plugin
def unload(name):
	del(loadedPlugins[name])

# Runs an individual plugin print function
def printPlugin(name,printer):
    try:
        printer.text("\n")
        loadedPlugins[name].print(printer)
        printer.text("\n")
    except Exception as e:
        handlers.err("running print for plugin " + name + " :: Exception raised :: " + str(e))

# Runs all plugins' print functions
def printAllPlugins(printer):
    for plugin in loadedPlugins:
        printPlugin(plugin,printer)
