Grab Fanart

About: 

This addon is intended a quick fix for XBMC Frodo behavior that was breaking some skins I liked to use. In Eden you could cycle through slideshows of your fanart by pointing to the Thumbnails/Video/Fanart or Thumbnails/Music/Fanart directories. With the new image caching system in Frodo a common directory for all fanart was no longer available and this broke a lot of really cool slideshow displays. 

This script uses the XBMC Database to find the source of the fanart files and downloads them to a common directory. You can point your skin/slideshows here. To create the file a CRC hash is created like XBMC would do internally, so only changed files are downloaded when doing an update. Old files are purged by keeping an internal array. This way you'll always have the most updated fanart. 

The Service: 

This addon automatically starts an XBMC service that will watch for video and music database update events. When a library scan finishes the grabber will attempt to find new fanart. In general this will work for 99% of cases, with the following caveats:

1) If you change fanart on a file you'll need a manual run, or wait for the next database update event to swap it in the grabber cache

2) If the database is cleaned this does not register as an update (in Gotham there is a Monitor for this) so after a clean you'll need a manual run or wait for the next database update event to clear the cache

3) TV and Movie database updated trigger 2 separate events. If they happen close together you may miss fanart from a new series/movie done by one of them. Again, do a manual update or wait for the next database update event. 

In general these scenerios will not hurt anything other than your fanart cache will not reflect your movie library until the next database update event is triggered. 

Using in skins or other programs:

You can call this addon using the RunScript(script.grab.fanart) internal function or the Addons.ExecuteAddon() method of the JSON-RPC interface. 

There is one optional parameter, related to if a progress bar dialog should be shown. This parameter will override the user setting for the progress bar, making it easy to hide the launching of the script if you wish. This is a simple "true" or "false" value - with true meaning "hide" and false meaning "use user default". It can be executed as: RunScript(script.grab.fanart, true). 
