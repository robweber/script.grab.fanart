import xbmc
import xbmcgui
from time import time
import json
import urllib
from random import randint
import resources.lib.utils as utils

class GrabFanartService:
    refresh_prop = 0 #when to refresh the properties
    refresh_media = 0 #when to refresh the media list
    
    WINDOW = None #object representing the home window
    xbmc_files = None #array representing media files
    
    def __init__(self):
        utils.log("Grab Fanart Service Started")

        #setup the window and file list
        self.WINDOW = xbmcgui.Window(10000)
        self.xbmc_files = list()
        
    def run(self):
        #keep this thread alive
        while(not xbmc.abortRequested):

            #check if the media list should be updated
            if(time() >= self.refresh_media):
                utils.log('Updating Media')
                if(utils.getSetting('mode') == 'random'):
                    self.grabRandom()
                else:
                    self.grabRecent()
                    
                    self.refresh_media = time() + (10 * 60)  #refresh again in 10 minutes

            if(time() >= self.refresh_prop and len(self.xbmc_files) > 0):
                total_found = len(self.xbmc_files) - 1

                fanart_index = randint(0,total_found)
                
                utils.log(self.xbmc_files[fanart_index].title)
                self.WINDOW.setProperty('script.grab.fanart.Title',self.xbmc_files[fanart_index].title)
                self.WINDOW.setProperty('script.grab.fanart.FanArt',self.xbmc_files[fanart_index].fan_art)
                    
                self.refresh_prop = time() + float(utils.getSetting("refresh"))
                
            xbmc.sleep(500)

    def grabRandom(self):
        mediatype = utils.getSetting('mediatype')
        self.xbmc_files = list()    #reset the list

        utils.log("media type is :" + mediatype)
        if(mediatype == 'videos' or mediatype == 'movies'):
            media_array = self.getJSON('VideoLibrary.GetMovies','{"properties":["title","fanart","year","file"]}')
            
            if(media_array != None and media_array.has_key('movies')):
                
                for aMovie in media_array['movies']:
                    newMedia = XbmcMedia()
                    newMedia.title = aMovie['title']
                    newMedia.fan_art = aMovie['fanart']

                    self.xbmc_files.append(newMedia)

        if(mediatype == 'videos' or mediatype == 'tvshows'):
            media_array = self.getJSON('VideoLibrary.GetTVShows','{"properties":["title","fanart","year","file"]}')

            if(media_array != None and media_array.has_key('tvshows')):
                
                for aShow in media_array['tvshows']:
                    newMedia = XbmcMedia()
                    newMedia.title = aShow['title']
                    newMedia.fan_art = aShow['fanart']

                    self.xbmc_files.append(newMedia)

        if(mediatype == 'music'):
            media_array = self.getJSON('AudioLibrary.GetArtists','{ "properties":["fanart"] }')

            if(media_array != None and media_array.has_key('artists')):

                for aArtist in media_array["artists"]:
                    newMedia = XbmcMedia()
                    newMedia.title = aArtist['artist']
                    newMedia.fan_art = aArtist['fanart']

                    self.xbmc_files.append(newMedia)

        utils.log("found " + str(len(self.xbmc_files)) + " files")

    def grabRecent(self):
        mediatype = utils.getSetting('mediatype')
        self.xbmc_files = list()    #reset the list

        utils.log("media type is :" + mediatype)
        if(mediatype == 'videos' or mediatype == 'movies'):
            media_array = self.getJSON('VideoLibrary.GetRecentlyAddedMovies','{"properties":["title","fanart","year","file"]}')
            
            if(media_array != None and media_array.has_key('movies')):
                
                for aMovie in media_array['movies']:
                    newMedia = XbmcMedia()
                    newMedia.title = aMovie['title']
                    newMedia.fan_art = aMovie['fanart']

                    self.xbmc_files.append(newMedia)

        if(mediatype == 'videos' or mediatype == 'tvshows'):
            media_array = self.getJSON('VideoLibrary.GetRecentlyAddedEpisodes','{"properties":["showtitle","fanart","file"]}')

            if(media_array != None and media_array.has_key('episodes')):
                
                for aShow in media_array['episodes']:
                    newMedia = XbmcMedia()
                    newMedia.title = aShow['showtitle']
                    newMedia.fan_art = aShow['fanart']

                    self.xbmc_files.append(newMedia)

        if(mediatype == 'music'):
            media_array = self.getJSON('AudioLibrary.GetRecentlyAddedAlbums','{ "properties":["artist","fanart"] }')

            if(media_array != None and media_array.has_key('artists')):

                for aArtist in media_array["albums"]:
                    newMedia = XbmcMedia()
                    newMedia.title = aArtist['artist']
                    newMedia.fan_art = aArtist['fanart']

                    self.xbmc_files.append(newMedia)

        utils.log("found " + str(len(self.xbmc_files)) + " files")

    def getJSON(self,method,params):
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "' + method + '" , "params" : ' + params + ' , "id":1 }')

        jsonobject = json.loads(json_response)
        
        if(jsonobject.has_key('result')):
            return jsonobject['result']
        else:
            utils.log("no result")
            return None


class XbmcMedia:
    title = ''
    fan_art = ''
    
GrabFanartService().run()
