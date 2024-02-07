import math
import pypot.dynamixel
from pypot.dynamixel.conversion import dxl_code
from pypot.dynamixel.conversion import dxl_decode
from time import sleep

from lib import Motor
import control_tables
from utils import read_from_file, dxl_decode_value, encode_signed

import matplotlib
import matplotlib.pyplot as plt
from utils import write_in_file
import numpy as np

from urchin import URDF

DXL_ID = 20
PORT = "/dev/ttyUSB0"
MASSE = 1.670 - 0.240  # Masse de l'objet en kg
DISTANCE = 0.45  # Distance de la masse à l'axe de rotation en mètres
GRAVITE = 9.81  # m/s²
input_tension = 12.78


configs = {
    "MX-106": {"resistance": 2.0, "torque_constant": 2.3593725498111775},
    "MX-64": {"resistance": 3.6, "torque_constant": 8.011176076962043},
}

dxl_io = pypot.dynamixel.Dxl320IO(PORT)
motor = Motor(dxl_io, DXL_ID, control_tables.MX_106, configs['MX-106']['resistance'], configs['MX-106']['torque_constant'], input_tension)

motor.torque_enabled = False
motor.mode = 0
motor.torque_enabled = True
motor.current = 0

last_position = motor.position

try:
    # print()
    # find_mass(motor)

    while True:
        # ajuster_position_moteur(motor)

        motor.current = float(input("mA: ")) / 1000
        sleep(.1)
        print(f"Measured current = {motor.current} A (should be 3.36mA)")
        

except KeyboardInterrupt:
    motor.motor_tension = 0
    motor.torque_enabled = False
