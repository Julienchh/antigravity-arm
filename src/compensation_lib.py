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
MASS = 0.08 # Object mass in kg
DISTANCE = 0.25 #8 #0.25  # Distance from the rotation axis in meters
GRAVITY = 9.81  # m/s²
OFFSET = 90.  # Offset in degrees
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

def compute_gravity_torque(mass, gravity, distance):
    """
    Return the torque needed to compensate the gravity force.
    mass: mass of the object in kg
    gravity: gravity acceleration in m/s²
    distance: distance from the rotation axis in meters
    """
    gravity_moment = mass * gravity * distance
    return gravity_moment

def friction(x):
    """
    Polynomial function to model the friction.
    """
    a, b, c, d, e, f, g, h  = [-0.12127746, -0.56061302, -0.47001329, -0.26110969, -0.13974794, 0.59132029, -0.4856983, 0.27422605]

    return np.where(x < 0, a * x ** 3 + b * x ** 2 + c * x + d, np.where(x > 0, e * x ** 3 + f * x ** 2 + g * x + h, 0))

def stribeck_model(omega):
    dynamic_friction_torque = -0.0011290596938334557
    stiction_torque = 0.22047280333906938
    stribeck_velocity = 0.3338122103926749
    viscous_friction_coefficient = 0.2392765860799163

    return (dynamic_friction_torque * np.sign(omega) + (stiction_torque - dynamic_friction_torque) * np.exp(-(omega / stribeck_velocity) ** 2)) * np.sign(omega) + dynamic_friction_torque + viscous_friction_coefficient * omega


def adjust_motor_position(motor):
    global last_position

    position = motor.position +OFFSET
    current_position = round(position, 1)
    eps = 0.1
    factor = 1

    gravity_torque = compute_gravity_torque(
        MASS, GRAVITY, DISTANCE
    ) + stribeck_model(motor.velocity * (np.pi / 30))

    if position - last_position > eps:
        gravity_torque *= -math.cos(math.radians(position))
    elif position - last_position < -eps:
        gravity_torque *= -math.sin(math.radians(position))

    if compensation_mode[motor.mode] == "tension":
        motor.torque = gravity_torque
    elif compensation_mode[motor.mode] == "current":
        motor.torque_current = gravity_torque
    elif compensation_mode[motor.mode] == "position":
        motor.goal_position = current_position + factor * gravity_torque - OFFSET

    last_position = position

input_tension = 12.78

""" # Lock all other motors when working on reachy
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
