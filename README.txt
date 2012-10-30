Grab Fanart

This addon is intended a quick fix for XBMC Frodo behavior that was breaking some skins I liked to use. In Eden you could cycle through slideshows of your fanart by pointing to the Thumbnails/Video/Fanart directories. with the new image caching system in Frodo a common directory for all fanart was no longer available and this broke a lot of really cool slideshow displays. 

This script uses the XBMC Database to find the source of the fanart files and downloads them to a common directory. You can point your skin/slideshows here. To create the file a CRC hash is created like XBMC would do internally, so only changed files are downloaded when doing an update. Old files are purged by keeping an internal array. This way you'll always have the most updated fanart. 
