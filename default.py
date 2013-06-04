from resources.lib.grabfanart import GrabFanart

if(len(sys.argv) > 1):
    if(sys.argv[1].lower() == 'true'):
        GrabFanart().run(True)
    elif(sys.argv[1].lower() == 'false'):
        GrabFanart().run()
else:
    GrabFanart().run()
            
