import xbmc
import xbmcgui
import json
import urllib
import xbmcvfs
import resources.lib.utils as utils

class GrabFanart:
    download_path = ''
    download_new = False
    
    def run(self):
        self.download_path = xbmc.translatePath(utils.getSetting('fanart_path'))

        self.download_path = self.download_path.replace('\\','/') #fix for slashes
        utils.log(self.download_path)

        if(utils.getSetting("download_new") == 'true'):
            self.download_new = True
            utils.log("Only downloading new fanart")
        
        #make sure the path exists
        if(self.download_path != '' and xbmcvfs.exists(self.download_path)):
            self.getMovies()
            self.getTVShows()
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
                image_name = item['title'].replace(" ",".") + "." + str(item['year']) + item['fanart'][-4:]
            
                #only download new and file exists, or we don't care
                if((self.download_new and self.fileExists(image_name) != 1) or not self.download_new):
                    utils.log(item['title'] + "." + str(item['year']))
                    xbmcvfs.copy(urllib.unquote(item['fanart'][8:]),self.download_path + image_name)
            else:
                utils.log("No fanart for: " + item['title'],xbmc.LOGDEBUG)

    def fileExists(self,fileName):
        return xbmcvfs.exists(self.download_path + fileName)
        
GrabFanart().run()
            
