from resources.lib.grabfanart import GrabFanart

grabber = GrabFanart()

if(len(sys.argv) > 1):
    if(sys.argv[1].lower() == 'true'):
        grabber.run("video",True)
        grabber.run("music",True)
    elif(sys.argv[1].lower() == 'false'):
        grabber.run("video")
        grabber.run("music")
else:
    grabber.run("video")
    grabber.run("music")
            
