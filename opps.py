from codrone_edu.drone import *

drone = Drone()
drone.pair()

#
# code goes here
#

drone.takeoff()
drone.set_throttle(50)
drone.move(2)

drone.set_throttle(5)
drone.set_pitch(25)
drone.move(5)

i=0
while i<20:
    if (i%2)==0:
        drone.set_drone_LED(255, 0, 0, 255)
        drone.drone_buzzer(Note.F4, 700)
    else:
        drone.set_drone_LED(0, 0, 255, 255)
        drone.drone_buzzer(Note.C4, 700)
    time.sleep(0.1)
    i+=1

drone.flip("right")
drone.land()

#

drone.close()