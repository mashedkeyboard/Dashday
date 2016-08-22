import pluginloader
from escpos import *

def testLoadPlugin():
    pluginloader.init('test')

    try:
       pluginloader.loadedPlugins['test']
    except NameError:
        raise NameError("Plugin loader is not defining the loaded plugins correctly")

    p = printer.Dummy()
    pluginloader.printPlugin('test',p)
    if str(p.output) != "I am a test. This is a test. Testing stuff. Test. Ta!":
        raise escpos.Error("Can't print test plugin successfully.")