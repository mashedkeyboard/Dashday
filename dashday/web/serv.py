from tg import expose, TGController, AppConfig, redirect
import configparser
import webhelpers2
import webhelpers2.text
from web.mtwsgi import make_server
import os
import dashday
import shutil

global nextRunTime
global userconfig
global firstrun

def getSubdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name)) and name != "__pycache__"]

class SetupController(TGController):
    mainconfig = configparser.ConfigParser()

    @expose('web/views/setup/index.xhtml')
    def index(self):
        global firstrun
        if firstrun != True:
            redirect('/')
        return {'firstrun': firstrun}

    @expose('web/views/setup/step1.xhtml')
    def step1(self):
        global firstrun
        if firstrun != True:
            redirect('/')
        return {'firstrun': firstrun}

    @expose()
    def doStep1(self, name, pvend, pprod):
        SetupController.mainconfig["General"] = {}
        SetupController.mainconfig["General"]["HelloMyNameIs"] = name
        SetupController.mainconfig["General"]["vendor"] = pvend
        SetupController.mainconfig["General"]["product"] = pprod
        with open('config/dashday.cfg.tmp', 'w') as dashdaycfg:
            SetupController.mainconfig.write(dashdaycfg)
        redirect('/setup/step2')

    @expose('web/views/setup/step2.xhtml')
    def step2(self):
        global firstrun
        with open('config/dashday.cfg.tmp', 'r') as dashdaycfg:
            confcode = dashdaycfg.read()
        if firstrun != True:
            redirect('/')
        return {'firstrun': firstrun, 'confcode': confcode}

    @expose()
    def doStep2(self, scheduleRun):
        SetupController.mainconfig["Schedule"] = {}
        SetupController.mainconfig["Schedule"]["runat"] = scheduleRun
        with open('config/dashday.cfg.tmp', 'w') as dashdaycfg:
            SetupController.mainconfig.write(dashdaycfg)
        redirect('/setup/step3')

    @expose('web/views/setup/step3.xhtml')
    def step3(self):
        global firstrun
        with open('config/dashday.cfg.tmp', 'r') as dashdaycfg:
            confcode = dashdaycfg.read()
        if firstrun != True:
            redirect('/')
        return {'firstrun': firstrun, 'confcode': confcode, 'pluginlist': getSubdirectories('plugins')}

    @expose()
    def doStep3(self, pluginSelect):
        SetupController.mainconfig["Plugins"] = {}
        SetupController.mainconfig["Plugins"]["toload"] = str(pluginSelect).strip('[]')
        with open('config/dashday.cfg.tmp', 'w') as dashdaycfg:
            SetupController.mainconfig.write(dashdaycfg)
        redirect('/setup/finish')

    @expose()
    def finish(self):
        global firstrun
        firstrun = False
        os.remove('config/dashday.cfg.tmp')
        with open('config/dashday.cfg', 'w') as dashdaycfg:
            SetupController.mainconfig.write(dashdaycfg)
        dashday.reload()
        redirect('/', {'update': 'true'})

class RootController(TGController):

    @expose('web/views/index.xhtml')
    def index(self, update = '', reload = ''):
        global firstrun
        if firstrun == True:
            redirect('/setup/')
        global nextRunTime
        return {'nextRun': nextRunTime, 'update': update, 'reload': reload}

    @expose('web/views/settings.xhtml')
    def settings(self):
        mainconfig = configparser.ConfigParser()
        try:
            mainconfig.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        return {'runTime': mainconfig["Schedule"]["runat"],
                'name': mainconfig["General"]["HelloMyNameIs"],
                'pvend': mainconfig["General"]["Vendor"],
                'pprod': mainconfig["General"]["Product"]}

    @expose('web/views/plugins.xhtml')
    def plugins(self,enable = '',disable = '',delete = ''):
        def pclass(plugin,enabledlist):
            if plugin in enabledlist:
                return {'class': 'success'}
            else:
                return {'class': 'none'}

        def getplugininfo(plugin):
            pinfo = __import__('plugins.' + plugin,fromlist=plugin)
            return {'name': pinfo.name,
                    'descrip': pinfo.description,
                    'version': pinfo.version,
                    'author': pinfo.author,
                    'cfgfile': pinfo.configfile}

        mainconfig = configparser.ConfigParser()
        try:
            mainconfig.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        pluginlist = mainconfig['Plugins']['toload'].split(',')
        return {'enabled': pluginlist,
                'all': getSubdirectories('plugins'),
                'pclass': pclass,
                'getpinfo': getplugininfo,
                'enable': enable,
                'disable': disable,
                'delete': delete}

    @expose()
    def enablePlugin(self, pid):
        mainconfig = configparser.ConfigParser()
        try:
            mainconfig.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        pluginlist = mainconfig['Plugins']['toload'].split(',')
        if pluginlist[0] != '':
            pluginlist.append(pid)
        else:
            pluginlist = [pid]
        mainconfig['Plugins']['toload'] = ', '.join(pluginlist)
        with open('config/dashday.cfg', 'w') as dashdaycfg:
            mainconfig.write(dashdaycfg)
        dashday.reload()
        redirect('/plugins', {'enable': 'true'})

    @expose()
    def deletePlugin(self, pid):
        shutil.rmtree('plugins/' + pid)
        dashday.reload()
        redirect('/plugins', {'delete': 'true'})

    @expose()
    def disablePlugin(self, pid):
        mainconfig = configparser.ConfigParser()
        try:
            mainconfig.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        pluginlist = mainconfig['Plugins']['toload'].split(',')
        pluginlist.remove(pid)
        mainconfig['Plugins']['toload'] = ', '.join(pluginlist)
        with open('config/dashday.cfg', 'w') as dashdaycfg:
            mainconfig.write(dashdaycfg)
        dashday.reload()
        redirect('/plugins', {'disable': 'true'})

    @expose()
    def changeTime(self, scheduleRun):
        mainconfig = configparser.ConfigParser()
        try:
            mainconfig.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        mainconfig["Schedule"]["runat"] = scheduleRun
        with open('config/dashday.cfg', 'w') as dashdaycfg:
            mainconfig.write(dashdaycfg)
        dashday.reload()
        redirect('/', {'update': 'true'})

    @expose()
    def changeGeneral(self, name, pvend, pprod):
        mainconfig = configparser.ConfigParser()
        try:
            mainconfig.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        mainconfig["General"]["HelloMyNameIs"] = name
        mainconfig["General"]["vendor"] = pvend
        mainconfig["General"]["product"] = pprod
        with open('config/dashday.cfg', 'w') as dashdaycfg:
            mainconfig.write(dashdaycfg)
        dashday.reload()
        redirect('/', {'update': 'true'})

    @expose()
    def reload(self):
        dashday.reload()
        redirect('/', {'reload': 'true'})

    setup = SetupController()

def init(isfirst = False):
    global userconfig
    global nextRunTime
    global firstrun
    firstrun = isfirst
    if os.path.isfile('config/web.cfg') == True:
        userconfig = configparser.ConfigParser()
        try:
            userconfig.read('config/web.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on web.cfg. Please ensure you have write permissions for the directory.")
    else:
        print("No configuration file found. Please configure Dashday's server.")
        exit()
    nextRunTime = "loading..."
    

def run():
    global userconfig
    global httpd
    config = AppConfig(minimal=True, root_controller=RootController())
    config['helpers'] = webhelpers2
    config.renderers = ['kajiki']
    config.serve_static = True
    config.paths['static_files'] = 'web/public'
    application = config.make_wsgi_app()

    print("Serving on port " + userconfig['Web']['porttoserve'] + "...")
    httpd = make_server('', int(userconfig['Web']['porttoserve']), application, 3)
    httpd.serve_forever()

def updateScheduledRun(newtime):
    global nextRunTime
    nextRunTime = newtime

def shutdown():
    global httpd
    httpd.shutdown()
    exit()