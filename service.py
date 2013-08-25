import xbmc
import xbmcgui
import thread
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

            if(time() >= self.refresh_prop):

                aVideo = None
                if(len(self.xbmc_movies) > 0):
                    random_index = self.randomNum(len(self.xbmc_movies))
                    
                    utils.log(self.xbmc_movies[random_index].title,xbmc.LOGDEBUG)
                    self.WINDOW.setProperty('script.grab.fanart.Movie.Title',self.xbmc_movies[random_index].title)
                    self.WINDOW.setProperty('script.grab.fanart.Movie.FanArt',self.xbmc_movies[random_index].fan_art)
                    self.WINDOW.setProperty('script.grab.fanart.Movie.Poster',self.xbmc_movies[random_index].poster)
                    self.WINDOW.setProperty('script.grab.fanart.Movie.Plot',self.xbmc_movies[random_index].plot)
                    
                    aVideo = self.xbmc_movies[random_index]
                    
                if(len(self.xbmc_tv) > 0):
                    random_index = self.randomNum(len(self.xbmc_tv))
                    
                    utils.log(self.xbmc_tv[random_index].title,xbmc.LOGDEBUG)
                    self.WINDOW.setProperty('script.grab.fanart.TV.Title',self.xbmc_tv[random_index].title)
                    self.WINDOW.setProperty('script.grab.fanart.TV.FanArt',self.xbmc_tv[random_index].fan_art)
                    self.WINDOW.setProperty('script.grab.fanart.TV.Poster',self.xbmc_tv[random_index].poster)
                    self.WINDOW.setProperty('script.grab.fanart.TV.Plot',self.xbmc_tv[random_index].plot)

                    #this will only have a value when "recent" is the type
                    self.WINDOW.setProperty('script.grab.fanart.TV.Season',str(self.xbmc_tv[random_index].season))
                    self.WINDOW.setProperty('script.grab.fanart.TV.Episode',str(self.xbmc_tv[random_index].episode))
                    self.WINDOW.setProperty('script.grab.fanart.TV.Thumb',self.xbmc_tv[random_index].thumb)
                    

                    #use a tv show if blank or randomly selected is = 9 (10% chance)
                    if(aVideo == None or self.randomNum(10) == 9):
                        aVideo = self.xbmc_tv[random_index]

                if(aVideo != None):
                    self.WINDOW.setProperty('script.grab.fanart.Video.Title',aVideo.title)
                    self.WINDOW.setProperty('script.grab.fanart.Video.FanArt',aVideo.fan_art)
                    self.WINDOW.setProperty('script.grab.fanart.Video.Poster',aVideo.poster)
                    self.WINDOW.setProperty('script.grab.fanart.Video.Plot',aVideo.plot)

                if(len(self.xbmc_music) > 0):
                    random_index = self.randomNum(len(self.xbmc_music))
                    
                    utils.log(self.xbmc_music[random_index].title,xbmc.LOGDEBUG)
                    self.WINDOW.setProperty('script.grab.fanart.Music.Artist',self.xbmc_music[random_index].title)
                    self.WINDOW.setProperty('script.grab.fanart.Music.FanArt',self.xbmc_music[random_index].fan_art)
                    self.WINDOW.setProperty('script.grab.fanart.Music.Description',self.xbmc_music[random_index].plot)
                    
                self.refresh_prop = time() + float(utils.getSetting("refresh"))


            #check if the media list should be updated
            if(time() >= self.refresh_media):
                if(utils.getSetting('mode') == 'random'):
                    thread.start_new_thread(self.grabRandom,())
                else:
                    thread.start_new_thread(self.grabRecent,())
                    
                self.refresh_media = time() + (60 * 60)  #refresh again in 60 minutes
                    
            xbmc.sleep(500)

    def grabRandom(self):
        self.xbmc_movies = list()    #reset the list
        self.xbmc_tv = list()
        self.xbmc_music = list()

        utils.log("media type is: random")
        
        media_array = self.getJSON('VideoLibrary.GetMovies','{"properties":["title","art","year","file","plot"]}')
            
        if(media_array != None and media_array.has_key('movies')):
                
            for aMovie in media_array['movies']:
                newMedia = XbmcMedia()
                newMedia.title = aMovie['title']
                newMedia.plot = aMovie['plot']

                if(aMovie['art'].has_key('fanart')):
                    newMedia.fan_art = aMovie['art']['fanart']

                if(aMovie['art'].has_key('poster')):
                    newMedia.poster = aMovie['art']['poster']

                if(newMedia.verify()):
                    self.xbmc_movies.append(newMedia)
                
        utils.log("found " + str(len(self.xbmc_movies)) + " movies files")
        
        media_array = self.getJSON('VideoLibrary.GetTVShows','{"properties":["title","art","year","file","plot"]}')

        if(media_array != None and media_array.has_key('tvshows')):
                
            for aShow in media_array['tvshows']:
                newMedia = XbmcMedia()
                newMedia.title = aShow['title']
                newMedia.plot = aShow['plot']

                if(aShow['art'].has_key('fanart')):
                    newMedia.fan_art = aShow['art']['fanart']

                if(aShow['art'].has_key('poster')):
                    newMedia.poster = aShow['art']['poster']

                if(newMedia.verify()):
                    self.xbmc_tv.append(newMedia)

        utils.log("found " + str(len(self.xbmc_tv)) + " tv files")
        
        media_array = self.getJSON('AudioLibrary.GetArtists','{ "properties":["fanart","description"] }')

        if(media_array != None and media_array.has_key('artists')):

            for aArtist in media_array["artists"]:
                newMedia = XbmcMedia()
                newMedia.title = aArtist['artist']
                newMedia.fan_art = aArtist['fanart']
                newMedia.plot = aArtist['description']

                if(newMedia.verify()):
                    self.xbmc_music.append(newMedia)

        utils.log("found " + str(len(self.xbmc_music)) + " music files")

    def grabRecent(self):
        self.xbmc_movies = list()    #reset the list
        self.xbmc_tv = list()
        self.xbmc_music = list()

        utils.log("media type is: recent")
        
        media_array = self.getJSON('VideoLibrary.GetRecentlyAddedMovies','{"properties":["title","art","year","file","plot"], "limits": {"end":10} }')
             
        if(media_array != None and media_array.has_key('movies')):
                
            for aMovie in media_array['movies']:
                newMedia = XbmcMedia()
                newMedia.title = aMovie['title']
                newMedia.plot = aMovie['plot']

                if(aMovie['art'].has_key('fanart')):
                    newMedia.fan_art = aMovie['art']['fanart']

                if(aMovie['art'].has_key('poster')):
                    newMedia.poster = aMovie['art']['poster']

                if(newMedia.verify()):    
                    self.xbmc_movies.append(newMedia)

        utils.log("found " + str(len(self.xbmc_movies)) + " movie files")
       
        media_array = self.getJSON('VideoLibrary.GetRecentlyAddedEpisodes','{"properties":["showtitle","art","file","plot","season","episode"], "limits": {"end":10} }')

        if(media_array != None and media_array.has_key('episodes')):
                
            for aShow in media_array['episodes']:
                newMedia = XbmcMedia()
                newMedia.title = aShow['showtitle']
                newMedia.plot = aShow['plot']
                newMedia.season = aShow['season']
                newMedia.episode = aShow['episode']
                
                if(aShow['art'].has_key('tvshow.fanart')):
                    newMedia.fan_art = aShow['art']['tvshow.fanart']

                if(aShow['art'].has_key('tvshow.poster')):
                    newMedia.poster = aShow['art']['tvshow.poster']

                if(aShow['art'].has_key('thumb')):
                    newMedia.thumb = aShow['art']['thumb']

                if(newMedia.verify()):
                    self.xbmc_tv.append(newMedia)

        utils.log("found " + str(len(self.xbmc_tv)) + " tv files")
        
        media_array = self.getJSON('AudioLibrary.GetRecentlyAddedAlbums','{ "properties":["artist","fanart"], "limits": {"end":10} }')

        if(media_array != None and media_array.has_key('albums')):

            for aArtist in media_array["albums"]:
                newMedia = XbmcMedia()
                newMedia.title = ",".join(aArtist['artist'])
                newMedia.fan_art = aArtist['fanart']

                if(newMedia.verify()):
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
    poster = ''
    plot = ''
    season = ''
    episode = ''
    thumb = ''

    def verify(self):
        result = True

        if(self.title == '' or self.fan_art == '' or self.poster == ''):
            result = False

        return result
    
GrabFanartService().run()
