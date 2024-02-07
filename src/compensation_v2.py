import math
import pypot.dynamixel
from pypot.dynamixel.conversion import dxl_code
from pypot.dynamixel.conversion import dxl_decode
from time import sleep

from lib import Motor
import control_tables
from utils import read_from_file, dxl_decode_value

import matplotlib
import matplotlib.pyplot as plt
from utils import write_in_file
import numpy as np


DXL_ID = 20
PORT = "/dev/ttyUSB0"
MASSE = 0.08 # Masse de l'objet en kg
DISTANCE = 0.25 #8 #0.25  # Distance de la masse à l'axe de rotation en mètres
GRAVITE = 9.81  # m/s²
OFFSET = 90.  # Offset de l'angle de la masse par rapport à l'axe de rotation en degrés
last_position = None
last_torque = None

# mass is at 26.5cm

configs = {
    "MX-106": {"resistance": 2.0, "torque_constant": 2.3593725498111775},
    "MX-64": {"resistance": 3.6, "torque_constant": 8.011176076962043},
}

motor_modes = {
    "current": 0,
    "velocity": 1,
    "position" : {"default" : 3 , "multi-turn" : 4},
    "pwm" : 16
}

compensation_mode = {
    0:"current", 16:"tension", 3:"position", 4:"position"
}

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

def friction(x, a, b, c, d, e, f, g, h):
    return np.where(x < 0, a * x ** 3 + b * x ** 2 + c * x + d, np.where(x > 0, e * x ** 3 + f * x ** 2 + g * x + h, 0))

def ajuster_position_moteur(motor):
    global last_position
    coeffs = [-0.12127746, -0.56061302, -0.47001329, -0.26110969, -0.13974794, 0.59132029, -0.4856983, 0.27422605]


    position = motor.position +OFFSET
    position_actuelle = round(position, 1)
    eps = 0.1
    facteur = 1

    couple_gravite = calculer_couple_contre_gravite(
        MASSE, GRAVITE, DISTANCE, position_actuelle
    ) + friction(motor.velocity * (np.pi / 30), *coeffs)

    if position - last_position > eps:
        couple_gravite *= -math.cos(math.radians(position))
    elif position - last_position < -eps:
        couple_gravite *= -math.sin(math.radians(position))

    if compensation_mode[motor.mode] == "tension":
        motor.torque = couple_gravite
    elif compensation_mode[motor.mode] == "current":
        motor.torque_current = couple_gravite
    elif compensation_mode[motor.mode] == "position":
        motor.goal_position = position_actuelle + facteur * couple_gravite - OFFSET

    last_position = position

def find_mass(motor):
    matplotlib.use("GTK3Agg")

    motor.motor_tension = 0
    motor.torque = 0.

    torques = []
    positions = []

    # 6.3
    for torque in range(0, 2000):
        motor.torque = torque / 1000

        # Use multi-sampling
        torques.append(motor.torque)
        positions.append(motor.motor_tension)
        print(f"Done {torques[-1]}")

        if torques[-1] >= 0.22:
            break


        # sleep(.3)

    torques = np.array(torques)
    positions = np.array(positions)

    write_in_file(torques, "torques.txt")
    write_in_file(positions, "positions.txt")

    fig, ax = plt.subplots()
    plt.plot(torques, positions, "yo", label="")
    plt.legend()

    plt.show()

input_tension = 12.78

""" # Lock all other motors
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
            input_tension
        )

        motor.torque_enabled = False
        motor.mode = 1
        motor.torque_enabled = True
        motor.goal_position = positions[index]

        print(f"Motor {motor_id} set")

torques = []
positions = [] """

# Setup shoulder
dxl_io = pypot.dynamixel.Dxl320IO(PORT)
motor = Motor(dxl_io, DXL_ID, control_tables.MX_106, configs['MX-106']['resistance'], configs['MX-106']['torque_constant'], input_tension)

motor.torque_enabled = False
# 16 = PWM, 1 = Velocity, 3 = Position
motor.mode = motor_modes["position"]["multi-turn"]
motor.torque_enabled = True
motor.current = 0

OFFSET -= motor.position

last_position = motor.position


try:
    # print()
    # find_mass(motor)
    #motor.PID = [1, 0, 0]

    while True:
        ajuster_position_moteur(motor)
        print(f"Position : {motor.position+OFFSET} degrees")
        # ajuster_position_moteur_cheat(motor)

        
except KeyboardInterrupt:
    
    motor.motor_tension = 0
    motor.torque_enabled = False
