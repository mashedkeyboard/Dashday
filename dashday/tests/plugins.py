import pluginloader
from escpos import *

def testLoadPlugin():
    pluginloader.init('test')

    try:
       pluginloader.loadedPlugins['test']
       if pluginloader.loadedPlugins['test'].init != True:
            raise NameError
    except NameError:
        raise NameError("Plugin loader is not defining the loaded plugins correctly")

    p = printer.Dummy()
    pluginloader.printPlugin('test',p)
    if p.output.decode("utf-8")  != "\x1bD\x04\rI am a test. This is a test. Testing stuff. Test. Ta!\x1bD\x04\r":
        raise escpos.Error("Can't print test plugin successfully.")