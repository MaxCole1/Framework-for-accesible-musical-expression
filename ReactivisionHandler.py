import tuio
import OSC

tracking = tuio.Tracking()

print "loaded profiles:", tracking.profiles.keys()
print "list functions to access tracked objects:", tracking.get_helpers()

class Listener(tuio.observer.AbstractListener):
    def notify(self, event):
        client = OSC.OSCClient()
        client.connect(('127.0.0.1', 6448))
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/wek/inputs")
        
        for obj in tracking.objects():
            oscmsg.append(obj.xpos)
            oscmsg.append(obj.ypos)
            oscmsg.append(obj.angle)
            oscmsg.append(obj.id)
                   
            print "Fiduccial ID: ", obj.id, " Position: ", obj.xpos , ", ", obj.ypos , " Angle ", obj.angle                 
            client.send(oscmsg)
        
if __name__ == "__main__":
    listener = Listener("Event Listener", tuio.getEventManager())
    tuio.mainLoop()
