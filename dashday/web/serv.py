from tg import expose, TGController, AppConfig, redirect
import configparser
import webhelpers2
import webhelpers2.text
from web.mtwsgi import make_server
import os
import dashday

global nextRunTime
global userconfig

class RootController(TGController):
    @expose('web/views/index.xhtml')
    def index(self,update = ''):
        global nextRunTime
        return {'nextRun': nextRunTime, 'update': update}

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

    @expose()
    def changeTime(self,scheduleRun):
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
    def changeGeneral(self,name,pvend,pprod):
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

def init():
    global userconfig
    global nextRunTime
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