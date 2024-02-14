import compensation_lib as cp


dxl_io = cp.pypot.dynamixel.Dxl320IO(cp.PORT)
motor = cp.Motor(dxl_io, cp.DXL_ID, cp.control_tables.MX_106, cp.configs['MX-106']['resistance'], cp.configs['MX-106']['torque_constant'], cp.input_tension)

motor.torque_enabled = False
motor.mode = cp.motor_modes["pwm"]
motor.torque_enabled = True
motor.motor_tension = 0

cp.OFFSET -= motor.position

cp.last_position = motor.position

try:
    motor.PID = [1, 0, 0]
    motor.FF = [0,0]
    
    while True:
        cp.adjust_motor_position(motor)
        print(f"Position : {motor.position+cp.OFFSET} degrees")

        
except KeyboardInterrupt:
    motor.motor_tension = 0
    motor.torque_enabled = False
