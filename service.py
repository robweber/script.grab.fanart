import xbmc
import resources.lib.utils as utils
from resources.lib.grabfanart import GrabFanart

class GrabFanartService:
    monitor = None
    run_grabber = False
    database = "video"
    
    def __init__(self):
        utils.log("Grab Fanart Service Started")
        self.monitor = DatabaseMonitor(monitor_method = self.databaseUpdated)

        #check for first time running
        if(utils.getSetting("first_run") == "true"):
            utils.log("First run, create cache")
            utils.setSetting("first_run","false")
            GrabFanart().run("video",True)
            GrabFanart().run("music",True)
        
    def run(self):
        #keep this thread alive
        while(not xbmc.abortRequested):
            
            if(self.run_grabber):
                utils.log("Grabbing Fanart")
                GrabFanart().run(self.database,True)
                self.run_grabber = False
                
            xbmc.sleep(500)

    def databaseUpdated(self,database):
        self.run_grabber = True
        self.database = database

class DatabaseMonitor(xbmc.Monitor):
    method_to_run = None

    def __init__(self,*args,**kwargs):
        xbmc.Monitor.__init__(self)
        self.method_to_run = kwargs['monitor_method']

    def onDatabaseUpdated(self,database):
        self.method_to_run(database)


GrabFanartService().run()
