from codrone_edu.drone import *

drone = Drone()
drone.pair()
drone.set_drone_LED(89,48,1,255)
drone.drone_buzzer(Note.C4, 1000)
drone.drone_buzzer(Note.D4, 1000)
drone.drone_buzzer(Note.E4, 1000)

drone.takeoff()
drone.set_throttle(50)
time.sleep(1.5)
drone.set_throttle(0)

drone.close()