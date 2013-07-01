Grab Fanart

About: 

This addon is intended a fix for XBMC Frodo behavior that was breaking some skins I liked to use. In Eden you could cycle through slideshows of your fanart by pointing to the Thumbnails/Video/Fanart or Thumbnails/Music/Fanart directories. With the new image caching system in Frodo a common directory for all fanart was no longer available and this broke a lot of really cool slideshow displays. 

This script uses the XBMC Database to find the source of the fanart files and exposes them via Window Properties so that skinners can still cycle through the art by referencing a single point of reference. 

Using This Addon: 

This addon is meant to be integrated as part of a skin. Currently it can be configured via addon settings in the Programs menu, or by calling the RunScript() function within a script. The parameters that can be set are: 

Refresh Time: How long between property updates. Default is 10 seconds
Media Type: movies, tv shows, videos (movies + tv) or music
Mode: Show fanart for recent items, or for random items

An example of setting these parameters using the RunScript function would be RunScript(script.grab.fanart,mode=random,mediatype=tvshows,refresh=10). If you want to include these settings are part of the regular skins settings you can pass these as parameters to RunScript upon hitting the home screen. 

Window Properties: 

Currently the service part of this addon will update Home window properties that can be used by skinners. These properties are refreshed according to the "refresh" interval. 

script.grab.fanart.Title - the title of the current media (Movie name, Show title, or Artist name)
script.grab.fanart.FanArt - the path to the fanart image for this media

To use this within a skin, an example would be $INFO[Window(Home).Property(script.grab.fanart.Title)] to show the media title. 