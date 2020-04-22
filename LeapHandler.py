import Leap, sys, thread, time, OSC
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class LeapMotionListener(Leap.Listener):
    finger_names = ["Thumb", "Index", "Middle","Ring", "Pinky"]
    bone_names = ["Metacarpal", "Proximal", "Intermediate", "Distal"]
    state_names = ["STATE_INVALID", "STATE_START", "STATE_UPDATE", "STATE_END"]

    def on_init(self, controller):
        print ("Listener initialised")

    def on_connect(self, controller):
        print ("Motion sensor connected!")

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE);
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP);
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE);

    def on_disconnect(self, controller):
        print ("Motion sensor disconnected")

    def on_exit(self, controller):
        print ("Exit")

    def on_frame(self, controller):

        frame = controller.frame()

        #Osc client initialisation
        client = OSC.OSCClient()
        client.connect(('127.0.0.1', 6448))
        oscmsg = OSC.OSCMessage()
        oscmsg.setAddress("/wek/inputs")
        

        #Hand data
        for hand in frame.hands:
            if (hand.is_left == True):
                handType = "Left Hand"
            else:
                handType = "Right Hand"

            print (handType + " Hand ID: " + str(hand.id) + " Palm position: " + str(hand.palm_position)) 

            normal = hand.palm_normal
            direction = hand.direction

            pitch = direction.pitch * Leap.RAD_TO_DEG
            roll = normal.roll * Leap.RAD_TO_DEG
            yaw = direction.yaw * Leap.RAD_TO_DEG
            
            for finger in hand.fingers:
                print("Finger ID: " + str(finger.id) + " " + self.finger_names[finger.type] + " Y position: " + str(finger.joint_position(3).y))
                oscmsg.append(finger.joint_position(3).y)

		    		
           
            print ("Pitch: " + str(pitch) + " Roll: " + str(roll) + " Yaw: " + str(yaw))
			
            oscmsg.append(hand.palm_position.x)
            oscmsg.append(hand.palm_position.y)
            oscmsg.append(hand.palm_position.z)
            oscmsg.append(pitch)
            oscmsg.append(roll)
            oscmsg.append(yaw)			
			
            client.send(oscmsg)

def main():

    listener = LeapMotionListener()
    controller = Leap.Controller()
    controller.add_listener(listener)

    print ("Press enter to quit")
    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass
    finally:
        controller.remove_listener(listener)

if __name__ == "__main__":
    main()

    
