Grab Fanart

About: 

This addon is intended a quick fix for XBMC Frodo behavior that was breaking some skins I liked to use. In Eden you could cycle through slideshows of your fanart by pointing to the Thumbnails/Video/Fanart directories. with the new image caching system in Frodo a common directory for all fanart was no longer available and this broke a lot of really cool slideshow displays. 

This script uses the XBMC Database to find the source of the fanart files and downloads them to a common directory. You can point your skin/slideshows here. To create the file a CRC hash is created like XBMC would do internally, so only changed files are downloaded when doing an update. Old files are purged by keeping an internal array. This way you'll always have the most updated fanart. 

Using in skins or other programs

You can call this addon using the RunScript(script.grab.fanart) internal function or the Addons.ExecuteAddon() method of the JSON-RPC interface. 

There is one optional parameter, related to if a progress bar dialog should be shown. This parameter will override the user setting for the progress bar, making it easy to hide the launching of the script if you wish. This is a simple "true" or "false" value - with true meaning "hide" and false meaning "use user default". It can be executed as: RunScript(script.grab.fanart, true). 
