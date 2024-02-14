from lib import Motor
import pypot
import control_tables
from utils import read_from_file
import numpy as np
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("GTK3Agg")

motor_id = 1
dxl_io = pypot.dynamixel.Dxl320IO("/dev/ttyUSB0", baudrate=57600)

motor = Motor(dxl_io, motor_id, control_tables.MX_64, 2.0, 12.78)
motor.caracterize()

tensions = np.array(read_from_file("tensions.txt"))
velocities = np.array(read_from_file("velocities.txt"))

slope, intercept = np.polyfit(velocities, tensions, 1)

print(f"Torque constant: {slope}")

plt.plot(velocities, tensions, "yo")
plt.plot(velocities.astype(int), slope * velocities.astype(int) + intercept, color='red', label='Linear regression')
plt.show()
