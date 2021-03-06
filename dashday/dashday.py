# Scheduling and web server and all sorts of fancy things!
import configparser
import web.serv
import schedule
import time
import main
import os
import threading

global dashdayjob
global configfile

def start():
    global dashdayjob
    print("Dashday started at " + time.strftime("%d/%m/%y %H:%M:%S"))    
    main.start()
    web.serv.updateScheduledRun(dashdayjob.next_run.strftime("%d/%m/%y %H:%M:%S"))
    print("Dashday completed, next scheduled launch is at " + dashdayjob.next_run.strftime("%d/%m/%y %H:%M:%S"))

def runapp():
    global dashdayjob
    global configfile
    dashdayjob = schedule.every().day.at(configfile['Schedule']['runat']).do(start)
    web.serv.updateScheduledRun(dashdayjob.next_run.strftime("%d/%m/%y %H:%M:%S"))
    print("Dashday service running, next scheduled launch is at " + dashdayjob.next_run.strftime("%d/%m/%y %H:%M:%S"))
    while True:
        schedule.run_pending()
        time.sleep(1)

def reload():
    global dashdayjob
    global configfile
    schedule.clear()
    if os.path.isfile('config/dashday.cfg') == True:
        configfile = configparser.ConfigParser()
        try:
            configfile.read('config/dashday.cfg')
        except PermissionError:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
    else:
        print("No configuration file found. Please configure Dashday.")
        exit()
    dashdayjob = schedule.every().day.at(configfile['Schedule']['runat']).do(start)
    web.serv.updateScheduledRun(dashdayjob.next_run.strftime("%d/%m/%y %H:%M:%S"))


if __name__ == "__main__":
    # Load the configuration file
    if os.path.isfile('config/dashday.cfg') == True:
        configfile = configparser.ConfigParser()
        try:
            configfile.read('config/dashday.cfg')
        except Exception as e:
            handlers.criterr("Permissions error on dashday.cfg. Please ensure you have write permissions for the directory.")
        web.serv.init()
        # Run the web server
        thr = threading.Thread(target=web.serv.run)
        thr.start()

        # Runs the scheduler and all that jazz
        thr = threading.Thread(target=runapp)
        thr.start()
    else:
        print("Please configure Dashday! Visit http://localhost:9375/ to start the setup.")
        web.serv.init(True)
        # Run the web server
        thr = threading.Thread(target=web.serv.run)
        thr.start()
