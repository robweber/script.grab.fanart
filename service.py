import xbmc
import resources.lib.utils as utils
from resources.lib.grabfanart import GrabFanart

class GrabFanartService:
    monitor = None
    run_grabber = False
    
    def __init__(self):
        utils.log("Grab Fanart Service Started")
        self.monitor = DatabaseMonitor(monitor_method = self.databaseUpdated)

        #keep this thread alive
        while(not xbmc.abortRequested):

            if(self.run_grabber):
                utils.log("Grabbing Fanart")
                GrabFanart().run(True)
                self.run_grabber = False
            xbmc.sleep(500)

    def databaseUpdated(self):
        self.run_grabber = True

class DatabaseMonitor(xbmc.Monitor):
    method_to_run = None

    def __init__(self,*args,**kwargs):
        xbmc.Monitor.__init__(self)
        self.method_to_run = kwargs['monitor_method']

    def onDatabaseUpdated(self,database):
        #only call if video database
        if(database == 'video'):
            self.method_to_run()


GrabFanartService()
