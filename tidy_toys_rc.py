# Tidy up the Toys - Manual control for driving using left analogue joystick with grabber control
# Bill Harvey 28 May 2021
# Last update 04 June 2021

# Need to add servo control for grabber up and down (once lift mech built)

from time import sleep
from approxeng.input.selectbinder import ControllerResource  # Import Approx Eng Controller libraries
import ThunderBorg3 as ThunderBorg
import UltraBorg3 as UltraBorg
# import os
import sys

global TB

# Setup the ThunderBorg
TB = ThunderBorg.ThunderBorg()
# TB.i2cAddress = 0x15                 # Uncomment and change the value if you have changed the board address
TB.Init()
if not TB.foundChip:
    boards = ThunderBorg.ScanForThunderBorg()
    if len(boards) == 0:
        print("No ThunderBorg found, check you are attached :)")
    else:
        print("No ThunderBorg at address %02X, but we did find boards:" % (TB.i2cAddress))
        for board in boards:
            print("    %02X (%d) " % (board, board))
        print("If you need to change the I2C address change the setup line so it is correct, e.g.")
        print("TB.i2cAddress = 0x%02X" % (boards[0]))
    sys.exit()
# Ensure the communications failsafe has been enabled!
failsafe = False
for i in range(5):
    TB.SetCommsFailsafe(True)
    failsafe = TB.GetCommsFailsafe()
    if failsafe:
        break
if not failsafe:
    print("Board %02X failed to report in failsafe mode!" % (TB.i2cAddress))
    sys.exit()

TB.MotorsOff()
TB.SetLedShowBattery(False)
TB.SetLeds(0, 0, 1)

# Start the UltraBorg
UB = UltraBorg.UltraBorg()  # Create a new UltraBorg object
UB.Init()  # Set the board up (checks the board is connected)

# Set servo to centre
UB.SetServoPosition1(-1.0)  # Test Servo positioning using ultra_gui.py to obtain start position and insert here
UB.SetServoPosition2(0) # Test Servo positioning using ultra_gui.py to obtain start position and insert here

def set_speeds(power_left, power_right):
    TB.SetMotor1(power_left)
    TB.SetMotor2(power_right)

def stop_motors():
    TB.MotorsOff()

def mixer(yaw, throttle, max_power=100):
    """
    Mix a pair of joystick axes, returning a pair of wheel speeds. This is where the mapping from
    joystick positions to wheel powers is defined, so any changes to how the robot drives should
    be made here, everything else is really just plumbing.

    :param yaw: 
        Yaw axis value, ranges from -1.0 to 1.0
    :param throttle: 
        Throttle axis value, ranges from -1.0 to 1.0
    :param max_power: 
        Maximum speed that should be returned from the mixer, defaults to 100
    :return: 
        A pair of power_left, power_right integer values to send to the motor driver
    """
    left = throttle + yaw
    right = throttle - yaw
    scale = float(max_power) / max(1, abs(left), abs(right))
    return int(left * scale), int(right * scale)

def main():
    print("Program controller loop started")
    while True:
        try:
            try:
                print("Use left and right joysticks to drive")
                print("Use Controller Square and Controller Circle to open / close grabber")
                print("Use Controller Triangle and Controller Cross to Lower / Lift grabber")
                with ControllerResource() as joystick:
                    print("Found a joystick and connected")
                    print(joystick.controls)
                    # Loop until joystick disconnects 
                    while joystick.connected:
                        # Get joystick values from the left analogue stick
                        x_axis, y_axis = joystick['lx', 'ly']
                        # Get power from mixer function
                        power_left, power_right = mixer(yaw=x_axis, throttle=y_axis)
                        # Set motor speeds
                        set_speeds(power_left, power_right)
                        
                        # Get joystick values from the left and right joysticks
                        #left_y = joystick["ly"]
                        # print("Left Joy")
                        #right_y = joystick["ry"]
                        # print("Right Joy")
                        #driveLeft = left_y
                        #driveRight = right_y

                        #TB.SetMotor1(driveRight)
                        #TB.SetMotor2(driveLeft)
                        
                        # Get a ButtonPresses object containing everything that was pressed since the last iteration of the loop
                        joystick.check_presses()
                        # Print any buttons that were pressed
                        if joystick.has_presses:
                            print(joystick.presses)

                        # Check for button presses since the last loop
                        presses = joystick.check_presses()
                        servo1 = 0
                        servo2 = 0
                        
                        if joystick.presses.square:
                            print("Square Pressed")
                            servo1 = -1.0
                            UB.SetServoPosition1(servo1)

                        if joystick.presses.circle:
                            print("Circle Pressed")
                            servo1 = -0.23
                            UB.SetServoPosition1(servo1)

                        if joystick.presses.triangle:
                            print("Triangle Pressed")
                            servo2 = -1.0
                            UB.SetServoPosition2(servo2)

                        if joystick.presses.triangle:
                            print("Cross Pressed")
                            servo2 = -0.23
                            UB.SetServoPosition2(servo2)

                        if joystick.has_presses:
                            print(joystick.presses)
                            servo1_pos = UB.GetServoPosition1()
                            print("servo 1 = ", servo1_pos)
                            servo2_pos = UB.GetServoPosition2()
                            print("servo 2 = ", servo2_pos)

                # Joystick disconnected.....
                print("Connection to joystick lost")

            except IOError:
                # No joystick found, wait for a bit and try again
                print("No joysticks found")
                # Set LEDs blue
                TB.SetLeds(0, 0, 1)
                sleep(1.0)
        except KeyboardInterrupt:
            # CTRL+C exit, give up
            print("\nUser aborted")
            TB.MotorsOff()
            TB.SetCommsFailsafe(False)
            TB.SetLeds(0, 0, 0)
            sys.exit()


main()
