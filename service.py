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
    xbmc_tv = None #array for tv shows
    xbmc_movies = None #array for movie files
    xbmc_music = None #array for music artist
    
    def __init__(self):
        utils.log("Grab Fanart Service Started")
        
        #setup the window and file list
        self.WINDOW = xbmcgui.Window(10000)
        self.xbmc_tv = list()
        self.xbmc_movies = list()
        self.xbmc_music = list()
        
    def run(self):
        #keep this thread alive
        while(not xbmc.abortRequested):

            #check if the media list should be updated
            if(time() >= self.refresh_media):
                if(utils.getSetting('mode') == 'random'):
                    self.grabRandom()
                else:
                    self.grabRecent()
                    
                    self.refresh_media = time() + (10 * 60)  #refresh again in 10 minutes

            if(time() >= self.refresh_prop):

                aVideo = None
                if(len(self.xbmc_movies) > 0):
                    random_index = self.randomNum(len(self.xbmc_movies))
                    
                    utils.log(self.xbmc_movies[random_index].title,xbmc.LOGDEBUG)
                    self.WINDOW.setProperty('script.grab.fanart.Movie.Title',self.xbmc_movies[random_index].title)
                    self.WINDOW.setProperty('script.grab.fanart.Movie.FanArt',self.xbmc_movies[random_index].fan_art)
                    aVideo = self.xbmc_movies[random_index]
                    
                if(len(self.xbmc_tv) > 0):
                    random_index = self.randomNum(len(self.xbmc_tv))
                    
                    utils.log(self.xbmc_tv[random_index].title,xbmc.LOGDEBUG)
                    self.WINDOW.setProperty('script.grab.fanart.TV.Title',self.xbmc_tv[random_index].title)
                    self.WINDOW.setProperty('script.grab.fanart.TV.FanArt',self.xbmc_tv[random_index].fan_art)

                    #use a tv show if blank or randomly selected is = 9 (10% chance)
                    if(aVideo == None or self.randomNum(10) == 9):
                        aVideo = self.xbmc_tv[random_index]

                if(aVideo != None):
                    self.WINDOW.setProperty('script.grab.fanart.Video.Title',aVideo.title)
                    self.WINDOW.setProperty('script.grab.fanart.Video.FanArt',aVideo.fan_art)

                if(len(self.xbmc_music) > 0):
                    random_index = self.randomNum(len(self.xbmc_music))
                    
                    utils.log(self.xbmc_music[random_index].title,xbmc.LOGDEBUG)
                    self.WINDOW.setProperty('script.grab.fanart.Music.Title',self.xbmc_music[random_index].title)
                    self.WINDOW.setProperty('script.grab.fanart.Music.FanArt',self.xbmc_music[random_index].fan_art)
                    
                self.refresh_prop = time() + float(utils.getSetting("refresh"))
                
            xbmc.sleep(500)

    def grabRandom(self):
        self.xbmc_movies = list()    #reset the list
        self.xbmc_tv = list()
        self.xbmc_music = list()

        utils.log("media type is: random")
        
        media_array = self.getJSON('VideoLibrary.GetMovies','{"properties":["title","fanart","year","file"]}')
            
        if(media_array != None and media_array.has_key('movies')):
                
            for aMovie in media_array['movies']:
                newMedia = XbmcMedia()
                newMedia.title = aMovie['title']
                newMedia.fan_art = aMovie['fanart']

                self.xbmc_movies.append(newMedia)
                
        utils.log("found " + str(len(self.xbmc_movies)) + " movies files")
        
        media_array = self.getJSON('VideoLibrary.GetTVShows','{"properties":["title","fanart","year","file"]}')

        if(media_array != None and media_array.has_key('tvshows')):
                
            for aShow in media_array['tvshows']:
                newMedia = XbmcMedia()
                newMedia.title = aShow['title']
                newMedia.fan_art = aShow['fanart']

                self.xbmc_tv.append(newMedia)

        utils.log("found " + str(len(self.xbmc_tv)) + " tv files")
        
        media_array = self.getJSON('AudioLibrary.GetArtists','{ "properties":["fanart"] }')

        if(media_array != None and media_array.has_key('artists')):

            for aArtist in media_array["artists"]:
                newMedia = XbmcMedia()
                newMedia.title = aArtist['artist']
                newMedia.fan_art = aArtist['fanart']

                self.xbmc_music.append(newMedia)

        utils.log("found " + str(len(self.xbmc_music)) + " music files")

    def grabRecent(self):
        self.xbmc_movies = list()    #reset the list
        self.xbmc_tv = list()
        self.xbmc_music = list()

        utils.log("media type is: recent")
        
        media_array = self.getJSON('VideoLibrary.GetRecentlyAddedMovies','{"properties":["title","fanart","year","file"], "limits": {"end":10} }')
             
        if(media_array != None and media_array.has_key('movies')):
                
            for aMovie in media_array['movies']:
                newMedia = XbmcMedia()
                newMedia.title = aMovie['title']
                newMedia.fan_art = aMovie['fanart']

                self.xbmc_movies.append(newMedia)

        utils.log("found " + str(len(self.xbmc_movies)) + " movie files")
       
        media_array = self.getJSON('VideoLibrary.GetRecentlyAddedEpisodes','{"properties":["showtitle","fanart","file"], "limits": {"end":10} }')

        if(media_array != None and media_array.has_key('episodes')):
                
            for aShow in media_array['episodes']:
                newMedia = XbmcMedia()
                newMedia.title = aShow['showtitle']
                newMedia.fan_art = aShow['fanart']

                self.xbmc_tv.append(newMedia)

        utils.log("found " + str(len(self.xbmc_tv)) + " tv files")
        
        media_array = self.getJSON('AudioLibrary.GetRecentlyAddedAlbums','{ "properties":["artist","fanart"], "limits": {"end":10} }')

        if(media_array != None and media_array.has_key('albums')):

            for aArtist in media_array["albums"]:
                newMedia = XbmcMedia()
                newMedia.title = ",".join(aArtist['artist'])
                newMedia.fan_art = aArtist['fanart']

                self.xbmc_music.append(newMedia)

        utils.log("found " + str(len(self.xbmc_music)) + " music files")

    def getJSON(self,method,params):
        json_response = xbmc.executeJSONRPC('{ "jsonrpc" : "2.0" , "method" : "' + method + '" , "params" : ' + params + ' , "id":1 }')

        jsonobject = json.loads(json_response)
        
        if(jsonobject.has_key('result')):
            return jsonobject['result']
        else:
            utils.log("no result")
            return None

    def randomNum(self,size):
        #return random number from 0 to x-1
        return randint(0,size -1)


class XbmcMedia:
    title = ''
    fan_art = ''
    
GrabFanartService().run()
