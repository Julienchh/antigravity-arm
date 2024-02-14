# The **source** folder

## File description

- `benchmark_*.ipynb`: Jupyter notebooks mainly used to do measures on the motors, trying to see if the commands sent to the firmware are really accurate. Also used to try to find the most accurate friction model.
- `compensation.py`: The script compensating the gravity. Can be used as it is.
- `lib.py | utils.py | control_tables.py`: Core library files for motor control.
- `torque_constant_measure.py`: Quick script to measure the motor constant $K_m$
