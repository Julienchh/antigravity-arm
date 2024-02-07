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

# from compensation_v2 import ajuster_position_moteur
last_position = None

PORT = '/dev/ttyACM0'
# with pypot.dynamixel.Dxl320IO(PORT) as dxl_io:
#     ids = dxl_io.scan()
#     print(ids)

DXL_ID = 10
# PORT = "/dev/ttyUSB2"
INPUT_TENSION = 12.78

configs = {
    "MX-106": {"resistance": 2.0, "torque_constant": 2.3593725498111775},
    "MX-64": {"resistance": 3.6, "torque_constant": 8.011176076962043},
}


# Lock all other motors
protocol_v2_motors = [11, 12, 13]
positions = [90, 180, 180]
with pypot.dynamixel.Dxl320IO(PORT) as dxl_io:
    for index, motor_id in enumerate(protocol_v2_motors):
        motor = Motor(
            dxl_io,
            motor_id,
            control_tables.MX_64,
            configs['MX-64']['resistance'],
            configs['MX-64']['torque_constant'],
            INPUT_TENSION
        )

        motor.torque_enabled = False
        motor.mode = 3
        motor.torque_enabled = True
        motor.goal_position = positions[index]

        print(f"Motor {motor_id} set")

# Setup shoulder
dxl_io = pypot.dynamixel.Dxl320IO(PORT)
motor = Motor(dxl_io, DXL_ID, control_tables.MX_106, configs['MX-106']['resistance'], configs['MX-106']['torque_constant'], INPUT_TENSION)

motor.torque_enabled = False
motor.mode = 16 # PWM Control mode
motor.torque_enabled = True
motor.motor_tension = 0

MASSE = 1.670 - 0.240  # Masse de l'objet en kg
DISTANCE = 0.405  # Distance de la masse à l'axe de rotation en mètres
GRAVITE = 9.81  # m/s²

couple_gravite = MASSE * DISTANCE * GRAVITE

sample_rate = 100 # Hz

time_samples = []
positions = []
current = []

sample_rate = 100 # Hz

time_samples = []
positions = []

def calculer_couple_contre_gravite(masse, gravite, distance, angle_degrees):
    """
    Retourne la force nécessaire pour contrebalancer la gravité.
    masse: masse de l'objet en kg
    gravite: accélération due à la gravité en m/s²
    distance: distance de la masse à l'axe de rotation en mètres
    angle_degrees: angle de l'axe de rotation en degrés
    """
    angle_radians = math.radians(angle_degrees)

    moment_gravite = masse * gravite * distance
    return moment_gravite

def ajuster_position_moteur(motor):
    global last_position

    position = motor.position
    position_actuelle = round(position, 1)
    eps = 0.1
    facteur = 1

    # print(f"{position - last_position}")
    couple_gravite = calculer_couple_contre_gravite(
        MASSE, GRAVITE, DISTANCE, position_actuelle
    )

    if position - last_position > eps:
        couple_gravite *= -math.cos(math.radians(position))
    elif position - last_position < -eps:
        couple_gravite *= -math.sin(math.radians(position))

    motor.torque = couple_gravite

    # print(f"Position actuelle: {position_actuelle}°")
    print(f"Couple gravité: {couple_gravite} N.m")
    # print(f"Tension nécessaire: {tension} V")
    # print(f"Tension actuelle: {motor.motor_tension}")
    # print(f"Courant actuel: {motor.current}")

    last_position = position

last_position = motor.position


print("Start")
try:
    date = time()
    elapsed = 0
    elapsed_since_start = 0
    while True:
        ajuster_position_moteur(motor)
        delta = (time() - date)
        date += delta
        elapsed += delta
        elapsed_since_start += delta
        # print(f"elapsed = {elapsed}")
        if elapsed >= 1/sample_rate:
            positions.append(motor.position)
            current.append(motor.current)
            time_samples.append(elapsed_since_start)
            elapsed = 0
            print(f"Position is {positions[-1]} ° at {time_samples[-1]} seconds")

except KeyboardInterrupt:
    write_in_file(time_samples, "pos_times.txt")
    write_in_file(positions, "pos_positions.txt")
    write_in_file(current, "pos_current.txt")