from pypot.dynamixel import Dxl320IO
from typing import List, Dict
from utils import to_signed, dxl_decode_value, dxl_encode_value, rpm_to_rad_s, write_in_file, encode_signed
from math import floor
import numpy as np
from time import sleep
from sympy.physics.units import amperes, volts

NB_SAMPLES = 5

pulses_per_resolution = 4096 # pulse/rev
pulses_per_degrees = 1 / 0.088
degrees_per_revolution = 360
degrees_per_pulse = degrees_per_revolution / pulses_per_resolution

class Motor:
    def __init__(self, dxl_io: Dxl320IO, motor_id: int, control_table: Dict[str, Dict[str, int]], resistance: float, torque_constant: float, input_voltage: float):
        self._dxl_io = dxl_io
        self._id = motor_id
        self._control_table = control_table
        self._resistance = resistance
        self._torque_constant = torque_constant
        self._input_voltage = input_voltage

    def _write_packet(self, control_table_entry, value: int) -> None:
        packet = self._dxl_io._protocol.DxlWriteDataPacket(
            self._id,
            control_table_entry["address"],
            dxl_encode_value(value, control_table_entry["size"]),
        )
        self._dxl_io._send_packet(packet)

    def _read_packet(self, control_table_entry) -> int:
        packet = self._dxl_io._protocol.DxlReadDataPacket(
            self._id, control_table_entry["address"], control_table_entry["size"]
        )
        response = self._dxl_io._send_packet(packet)

        return dxl_decode_value(response.parameters)
    
    @property
    def PID(self) -> List[float]:
        """
            The servomotor's PID values

            @return {List[float]}
        """
        pid = [self._read_packet(self._control_table["position P_gain"]), self._read_packet(self._control_table["position I_gain"]), self._read_packet(self._control_table["position D_gain"])]

        return pid
    
    @PID.setter
    def PID(self, values: List[float]) -> None:
        self._write_packet(self._control_table["position P_gain"], values[0])
        self._write_packet(self._control_table["position I_gain"], values[1])
        self._write_packet(self._control_table["position D_gain"], values[2])

    @property
    def motor_tension(self) -> float:
        # Seems OK
        return (self._input_voltage * self.pwm) / 100

    # Shit code
    @property
    def input_voltage(self) -> float:
        """
            The servomotor's current operating voltage (doesn't seem to work: inaccurate results)

            @returns {float} V
        """
        values = []

        for _ in range(NB_SAMPLES):
            values.append(self._read_packet(self._control_table["present_input_voltage"]))

        return np.median(values) * 0.1

    @motor_tension.setter
    def motor_tension(self, target_voltage: float) -> None:
        # Seems OK
        duty_cycle = (target_voltage / self._input_voltage) * 100
        self.pwm = encode_signed(floor(duty_cycle / 0.113))

    @property
    def back_emf(self) -> float:
        """
            The servomotor's current back EMF

            @return {float} %
        """
        velocity = self.velocity * (np.pi / 30)

        return self._torque_constant * velocity

    # @back_emf.setter
    # def back_emf(self, value: float) -> None:
    #     goal_vel = value / self._torque_constant
    #     self.goal_velocity = goal_vel

    @property
    def pwm(self) -> float:
        """
            The servomotor's current PWM setting

            @return {float} %
        """
        values = []

        for _ in range(NB_SAMPLES):
            values.append(self._read_packet(self._control_table["present_pwm"]))

        return np.median(values) * 0.113

    @pwm.setter
    def pwm(self, value: float) -> None:
        self._write_packet(self._control_table["goal_pwm"], value)

    @property
    def current(self) -> float:
        """
            The current used by the servomotor to operate

            @return {float} A
        """
        values = []

        for _ in range(NB_SAMPLES):
            values.append(to_signed(self._read_packet(self._control_table["present_current"])))

        return (np.median(values) * 3.36) / 1000

    @current.setter
    def current(self, value: float) -> None:
        """
            Sets the servomotor's goal current

            @param {float} A
        """
        self._write_packet(self._control_table["goal_current"], floor((value * 1000) / 3.36))

    @property
    def torque_enabled(self) -> bool:
        """
            Checks if the servomotor's torque is enabled

            @return {bool}
        """
        return bool(self._read_packet(self._control_table["torque_enable"]))

    @torque_enabled.setter
    def torque_enabled(self, value: bool) -> None:
        """
            Enables or disables the servomotor's torque

            @param {bool}
        """
        self._write_packet(self._control_table["torque_enable"], int(value))

    @property
    def torque(self) -> float:
        return ((self.motor_tension-self.back_emf) / self._resistance) * self._torque_constant

    @property
    def torque_current(self) -> float:
        return self.current * self._torque_constant

    @torque_current.setter
    def torque_current(self, value: float) -> None:
        if self.mode != 0: # Control via current only
            return

        self.current = value / self._torque_constant
    

    @torque.setter
    def torque(self, value) -> None:
        if self.mode != 16: # Control is done via PWM only
            return

        # print(f"Back emf : {self.back_emf} rad/s")
        self.motor_tension = (value / self._torque_constant) * self._resistance + self.back_emf

    @property
    def velocity_limit(self) -> float:
        """
            The servomotor's velocity limit

            @return {float} rpm
        """
        velocity_limit = self._read_packet(self._control_table["velocity_limit"])

        return velocity_limit * 0.229

    @property
    def goal_velocity(self) -> float:
        """
            The servomotor's goal velocity

            @return {float} rpm
        """
        goal_velocity = self._read_packet(self._control_table["goal_velocity"])

        return to_signed(goal_velocity) * 0.229

    @goal_velocity.setter
    def goal_velocity(self, value) -> None:
        self._write_packet(self._control_table["goal_velocity"], floor(value / 0.229))

    @property
    def velocity(self) -> float:
        """
            The servomotor's current velocity

            @return {float} rpm
        """
        values = []

        for _ in range(NB_SAMPLES):
            values.append(to_signed(self._read_packet(self._control_table["present_velocity"]), 32))

        return np.median(values) * 0.229 # rpm

    @property
    def mode(self) -> int:
        return self._read_packet(self._control_table["operating_mode"])

    @mode.setter
    def mode(self, value: int) -> None:
        self._write_packet(self._control_table["operating_mode"], value)

    @property
    def position(self) -> float:
        """
            The servomotor's position

            @return {float} deg
        """
        position = self._read_packet(self._control_table["present_position"])

        return position * degrees_per_pulse

    @property
    def goal_position(self) -> float:
        """
            The servomotor's goal position

            @return {float} deg/pulse
        """
        goal_position = self._read_packet(self._control_table["goal_position"])

        return goal_position * degrees_per_pulse
    
    @goal_position.setter
    def goal_position(self, value: float) -> None:
        self._write_packet(self._control_table["goal_position"], floor(value / degrees_per_pulse))

    @property
    def pwm_limit(self) -> int:
        pwm_limit = self._read_packet(self._control_table["pwm_limit"])

        return pwm_limit

    @pwm_limit.setter
    def pwm_limit(self, value) -> None:
        if value > 885:
            print(f"[PWM Limit] Value too high: {value}")
            return

        self._write_packet(self._control_table["pwm_limit"], value)


    def caracterize(self) -> None:
        # Setup motor
        self.torque = False
        self.mode = 1  # Velocity mode
        self.torque = True

        velocities = []
        tensions = []

        limit = floor(self.velocity_limit)

        for i in range(1, limit):
            print(f"{i} / {limit}")

            self.goal_velocity = i

            sleep(2)

            velocities.append(rpm_to_rad_s(self.velocity))
            tensions.append(self.motor_tension)

        # Reset motor
        self.goal_velocity = 0

        self._torque_constant, _ = np.polyfit(velocities, tensions, 1)

        write_in_file(velocities, "velocities.txt")
        write_in_file(tensions, "tensions.txt")
