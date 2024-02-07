import math
import pypot.dynamixel
from pypot.dynamixel.conversion import dxl_code
from pypot.dynamixel.conversion import dxl_decode
from time import sleep, time

from lib import Motor
import control_tables
from utils import read_from_file, dxl_decode_value

import matplotlib
import matplotlib.pyplot as plt
from utils import write_in_file
import numpy as np
# from compensation_v2 import configs
# Setup shoulder

configs = {
    "MX-106": {"resistance": 2.0, "torque_constant": 2.3593725498111775},
    "MX-64": {"resistance": 3.6, "torque_constant": 8.011176076962043},
}
PORT = "/dev/ttyUSB0"
# PORT = "/dev/ttyACM1"
DXL_ID = 20
# DXL_ID = 10
INPUT_TENSION = 12.78
dxl_io = pypot.dynamixel.Dxl320IO(PORT)
motor = Motor(dxl_io, DXL_ID, control_tables.MX_106, configs['MX-106']['resistance'], configs['MX-106']['torque_constant'], INPUT_TENSION)

motor.torque_enabled = False
motor.mode = 1 # PWM Control mode
motor.torque_enabled = True

MASSE = 1.670 - 0.240  # Masse de l'objet en kg
DISTANCE = 0.405  # Distance de la masse à l'axe de rotation en mètres
GRAVITE = 9.81  # m/s²

couple_gravite = MASSE * DISTANCE * GRAVITE

positions = []
time_samples = []

speed_packets = []

start_position = motor.position
elapsed_since_start = 0

speed_to_test = [2**n for n in range(6)]


avg_sampled_speed = []
avg_packet_speed = []
avg_reel_speed = []
try:
    date = time()

    execution_time = 10 # second
    for speed in speed_to_test:
        print(f"Speed = {speed} rpm")
        motor.goal_velocity = speed

        while elapsed_since_start < execution_time:


            positions.append(motor.position)
            time_samples.append(elapsed_since_start)
            speed_packets.append(motor.velocity)
            # compute timestamp
            delta = (time() - date)
            date += delta
            # clock
            elapsed_since_start += delta


        speeds = np.array([(positions[t] - positions[t-1]) / (time_samples[t] - time_samples[t-1]) for t in range(1, len(time_samples))])
        speeds = np.concatenate((np.array([0]), speeds))

        end_position = motor.position

        avg_reel_speed.append((end_position-start_position)/(6*elapsed_since_start))
        avg_packet_speed.append(np.average(speed_packets))
        avg_sampled_speed.append(np.average(speeds)/6)

        positions = []
        time_samples = []
        speed_packets = []

        elapsed_since_start = 0
        
        start_position = motor.position



except KeyboardInterrupt:
    motor.motor_tension = 0
    motor.torque_enabled = False

motor.goal_velocity = 0

write_in_file(avg_sampled_speed, "vel_loaded2_avg_sampled_speed.txt")
write_in_file(avg_packet_speed, "vel_loaded2_avg_packet_speed.txt")
write_in_file(avg_reel_speed, "vel_loaded2_avg_reel_speed.txt")
