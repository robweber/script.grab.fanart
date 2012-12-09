import xbmc
import xbmcgui
import json
import urllib
import xbmcvfs
import resources.lib.utils as utils

class GrabFanart:
    download_path = ''
    current_files = []
    ignore_files = []
    
    progressBar = None
    filesLeft = 0
    filesTotal = 1
    
    def run(self):
        self.download_path = xbmc.translatePath(utils.getSetting('fanart_path'))

        self.download_path = self.download_path.replace('\\','/') #fix for slashes
        utils.log(self.download_path)
        
        #make sure the path exists
        if(self.download_path != ''):

            if(not xbmcvfs.exists(self.download_path)):
                #ask if the path should be created
                if(xbmcgui.Dialog().yesno(utils.getString(30010),utils.getString(30020))):
                    xbmcvfs.mkdir(self.download_path)
                else:
                    return
            
            #open the progress bar
            if(utils.getSetting("run_silent") == "false"):
                self.progressBar = xbmcgui.DialogProgress()
                self.progressBar.create(utils.getString(30010),"Copying Files")

            #check if there are any ignore paths
            if(utils.getSetting("ignore_paths") != ''):
                self.ignore_files = utils.getSetting("ignore_paths").split(',')
 
            #get new files
            self.getMovies()
            self.getTVShows()

            #clean old files
            self.cleanOld()

            #close the progress bar
            if(utils.getSetting("run_silent") == "false"):
                self.progressBar.close()
        else:
             xbmcgui.Dialog().ok(utils.getString(30010),utils.getString(30020))

    def getTVShows(self):
        utils.log('Running get tv shows')
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "VideoLibrary.GetTVShows" , "params" : {"properties":["title","fanart","year","file"]} , "id":1 }')

        jsonobject = json.loads(json_response)
    
        if(jsonobject.has_key('result')):
            try:
                self.copyFiles(jsonobject['result']['tvshows'])
            except KeyError:
                pass
            
    def getMovies(self):
        utils.log('Running get movies')
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "VideoLibrary.GetMovies" , "params" : {"properties":["title","fanart","year","file"]} , "id":1 }')

        jsonobject = json.loads(json_response)
    
        if(jsonobject.has_key('result')):
            try:
                self.copyFiles(jsonobject['result']['movies'])
            except KeyError:
                pass
            
    def copyFiles(self,jsonresult):
        
        utils.log("Found " + str(len(jsonresult)) + " objects")
        self.filesLeft = self.filesLeft + len(jsonresult)
        self.filesTotal = self.filesTotal + len(jsonresult)
        
        for item in jsonresult:
            self.updateProgress()

            valid_file = True

            #if the path is not in the ignore list
            for files in self.ignore_files:
                if(files in item['file']):
                    valid_file = False
                    
            if(item.has_key('fanart') and item['fanart'] != '' and valid_file):
                file_url = urllib.unquote(item['fanart'][8:])

                #check if trailing slash is included
                if(file_url[-1:] == "/"):
                    file_url = file_url[:-1]
                    
                #create the filename
                image_name = self.createCRC(file_url)

                #add to internal list
                self.current_files.append(image_name + ".tbn")
                
                #get the file if it doesn't exist
                if(not xbmcvfs.exists(self.download_path + image_name + ".tbn")):
                    utils.log(item['title'] + " " + str(item['year']))
                    xbmcvfs.copy(file_url,self.download_path + image_name + ".tbn")
            else:
                utils.log("No fanart for: " + item['title'],xbmc.LOGDEBUG)
                
    def cleanOld(self):
        fileSet = set(self.current_files)
        
        #get a list of files from this directory
        dirs,files = xbmcvfs.listdir(self.download_path)

        #delete any files that aren't in the current file list
        for aFile in files:
            if not aFile in fileSet:
               xbmcvfs.delete(self.download_path + aFile)

    def updateProgress(self):
        self.filesLeft = self.filesLeft -1

        if(utils.getSetting("run_silent") == 'false'):
            self.progressBar.update(int((float(self.filesTotal - self.filesLeft)/float(self.filesTotal)) * 100),"Copying Files")
            
    #code from XBMC wiki
    def createCRC(self, string):
        string = string.lower()        
        bytes = bytearray(string.encode())
        crc = 0xffffffff;
        for b in bytes:
            crc = crc ^ (b << 24)          
            for i in range(8):
                if (crc & 0x80000000 ):                 
                    crc = (crc << 1) ^ 0x04C11DB7                
                else:
                    crc = crc << 1;                        
                    crc = crc & 0xFFFFFFFF
        
        return '%08x' % crc
        
GrabFanart().run()
            
