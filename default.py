import xbmc
import xbmcgui
import json
import urllib
import xbmcvfs
import resources.lib.utils as utils

class GrabFanart:
    download_path = ''
    current_files = []
    
    def run(self):
        self.download_path = xbmc.translatePath(utils.getSetting('fanart_path'))

        self.download_path = self.download_path.replace('\\','/') #fix for slashes
        utils.log(self.download_path)
        
        #make sure the path exists
        if(self.download_path != '' and xbmcvfs.exists(self.download_path)):
            #get new files
            self.getMovies()
            self.getTVShows()

            #clean old files
            self.cleanOld()
        else:
             xbmcgui.Dialog().ok(utils.getString(30010),utils.getString(30020))

    def getTVShows(self):
        utils.log('Running get tv shows')
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "VideoLibrary.GetTVShows" , "params" : {"properties":["title","fanart","year"]} , "id":1 }')

        jsonobject = json.loads(json_response)
    
        if(jsonobject.has_key('result')):
            self.copyFiles(jsonobject['result']['tvshows'])
            
    def getMovies(self):
        utils.log('Running get movies')
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "VideoLibrary.GetMovies" , "params" : {"properties":["title","fanart","year"]} , "id":1 }')

        jsonobject = json.loads(json_response)
    
        if(jsonobject.has_key('result')):
            self.copyFiles(jsonobject['result']['movies'])
            
    def copyFiles(self,jsonresult):
        
        utils.log("Found " + str(len(jsonresult)) + " objects")
        for item in jsonresult:
            if(item.has_key('fanart') and item['fanart'] != ''):
                #create the filename
                image_name = self.createCRC(urllib.unquote(item['fanart'][8:]))

                #add to internal list
                self.current_files.append(image_name + ".tbn")
                
                #get the file if it doesn't exist
                if(not xbmcvfs.exists(self.download_path + image_name + ".tbn")):
                    utils.log(item['title'] + " " + str(item['year']))
                    xbmcvfs.copy(urllib.unquote(item['fanart'][8:]),self.download_path + image_name + ".tbn")
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
            
