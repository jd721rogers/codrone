from codrone_edu.drone import *
from PIRController import *
from SensorData import *
from DataLogger import *
import keyboardInput

keyboardInput.listen_for_keys()


# Initialize time
update_dt = 1.0 / 2.0  # 15 Hz
t_end = 1000

# Connect to the drone
drone = Drone()
drone.pair()

# Get the current time
t_prev = time.time()
t_end = t_prev + t_end

# Initialize the sensor data class
sensors = SensorData(drone)

# Open and initialize the log file
log_file_name = "altitude_control_75_I5.txt"
LOG_DATA = 1
header = ["time", "altitude", "velocityX", "velocityY", "altitude_cmd", "velocityX_cmd", "velocityY_cmd", "throttle_cmd"]
log = DataLogger(log_file_name, header, LOG_DATA)

# Initialize the altitude controller
kp_alt = 50.0
ki_alt = 4.0
kd_alt = 0.0
pir_alt = PIRController(kp_alt, ki_alt, kd_alt, -75, 75, t_prev)

# Initialize the X velocity controller
kp_vx = 1.5
ki_vx = 0.25
kd_vx = 0.0
pir_vx = PIRController(kp_vx, ki_vx, kd_vx, -75, 75, t_prev)

# Initialize the y velocity controller
kp_vy = 1.5
ki_vy = 0.25
kd_vy = 0.0
pir_vy = PIRController(kp_vy, ki_vy, kd_vy, -75, 75, t_prev)

input("Press Enter to take off...")

# Update sensor data to get altitude (nonsense dt input because we don't need velocity yet)
# Repeat until a valid baro altitude is received
sensors.update_alt_data()
while sensors.baroAltitude == 0:
    sensors.update_alt_data()

# Save off the launch barometric altitude
altitude0 = sensors.baroAltitude
print("Takeoff altitude (asl): ", altitude0)

# Takeoff
drone.takeoff()
drone.set_throttle(0.0)

# Set logical flags
first_time = True

# Set initial commands
altitude_cmd = 1.5 # m
vx_cmd = 0.0
vy_cmd = 0.0

print("Press q to land")
while True:

    # Update time
    t = time.time()

    # Break and land if flight has exceeded the allotted time
    if t > t_end:
        break

    # Break and land if q is pressed on the keyboard
    if keyboardInput.stop_flag:
        print("Loop terminated by user.")
        break

    # Loop through and update commands at specified rate
    if t - t_prev >= update_dt:

        # Calculate dt
        dt = t - t_prev
        # Update previous time
        t_prev = t

        # Control altitude
        # -----------------------------------------------------------------------
        # Get the updated altitude data
        sensors.update_alt_data()
        altitude = sensors.baroAltitude
        # Run the PIR altitude controller
        throttle_cmd = pir_alt.pir(altitude_cmd, altitude - altitude0, 0.0, t)
        # Set "Throttle" which really commands an up/down velocity
        drone.set_throttle(throttle_cmd)  # Throttle from -100-100

        # Determine velocity and heading commands for obstacle avoidance
        # ---------------------------------------------------------------------
        # Get accel/gyro/attitude data
        sensors.update_motion_data()
        # Get velocity data
        sensors.update_velocity_data()

        # Control x velocity
        vx = sensors.velocity_x
        ax = sensors.accelX
        pitch_power = pir_vx.pir(vx_cmd, vx, 0.0, t)
        drone.set_pitch(pitch_power)

        # Control y velocity
        vy = sensors.velocity_y
        ay = sensors.accelY
        roll_power = pir_vy.pir(vy_cmd, vy, 0.0, t)
        drone.set_roll(roll_power)

        # Write the output
        print("Altitude: ", altitude - altitude0, ", Vx: ", vx, ", Vy: ", vy, "ay: ", ay, "roll_power: ", roll_power)
        data = [sensors.time, altitude-altitude0, vx, vy, altitude_cmd, vx_cmd, vy_cmd, throttle_cmd]
        log.write_data(data)

        drone.move()

drone.land()



