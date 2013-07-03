Grab Fanart

About: 

This addon is intended a fix for XBMC Frodo behavior that was breaking some skins I liked to use. In Eden you could cycle through slideshows of your fanart by pointing to the Thumbnails/Video/Fanart or Thumbnails/Music/Fanart directories. With the new image caching system in Frodo a common directory for all fanart was no longer available and this broke a lot of really cool slideshow displays. 

This script uses the XBMC Database to find the source of the fanart files and exposes them via Window Properties so that skinners can still cycle through the art by referencing a single point of reference. 

Using This Addon: 

This addon is meant to be integrated as part of a skin. Currently it can be configured via addon settings in the Programs menu, or by calling the RunScript() function within a script. The parameters that can be set are: 

Refresh Time: How long between property updates. Default is 10 seconds
Mode: Show fanart for recent items (10), or for random items

An example of setting these parameters using the RunScript function would be RunScript(script.grab.fanart,mode=random,refresh=10). If you want to include these settings are part of the regular skins settings you can pass these as parameters to RunScript upon hitting the home screen. 

Window Properties: 

Currently the service part of this addon will update Home window properties that can be used by skinners. These properties are refreshed according to the "refresh" interval. 

script.grab.fanart.Video.Title - the title of a random video (movie or tv show). There is a 25% chance of this being a TV show. 
script.grab.fanart.Video.FanArt - the path to the fanart image for this video
script.grab.fanart.Movie.Title - title of the selected movie
script.grab.fanart.Movie.FanArt - path to movie fanart
script.grab.fanart.TV.Title - title of selected tv show
script.grab.fanart.TV.FanArt - path to tv show fanart
script.grab.fanart.Music.Title - music artist name
script.grab.fanart.Music.FanArt - path to artist fanart 

To use this within a skin, an example would be $INFO[Window(Home).Property(script.grab.fanart.Video.Title)] to show the media title. 