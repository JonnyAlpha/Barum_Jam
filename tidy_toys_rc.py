# Tidy up the Toys - Manual control for driving using left analogue joystick with grabber control
# Bill Harvey 28 May 2021
# Last update 18 June 2021

# Servo 3 = open / close grabber
# Servo 4 = raise / lower grabber

from time import sleep
from approxeng.input.selectbinder import ControllerResource  # Import Approx Eng Controller libraries
import ThunderBorg3 as ThunderBorg
import UltraBorg3 as UltraBorg
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

# Set servo start positions
UB.SetServoPosition3(0)  # Test Servo positioning using ultra_gui.py to obtain start position and insert here
UB.SetServoPosition4(0.33) # Test Servo positioning using ultra_gui.py to obtain start position and insert here

def set_speeds(power_left, power_right):
    TB.SetMotor1(power_left/100)
    TB.SetMotor2(power_right/100)

def stop_motors():
    TB.MotorsOff()

def mixer(yaw, throttle, max_power=50): #reduced max_power from 100 to 50
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

    left = throttle - yaw # was +
    right = throttle + yaw # was -
    scale = float(max_power) / max(1, abs(left), abs(right))
    return int(left * scale), int(right * scale)

def main():
    print("Program controller loop started")
    while True:
        try:
            try:
                with ControllerResource() as joystick:
                    print("Found a joystick and connected")
                    print(joystick.controls)
                    print("Use left joystick to drive")
                    print("Use Controller Square and Controller Circle to open / close grabber - Servo 3")
                    print("Use Controller Triangle and Controller Cross to Lower / Lift grabber - Servo 4")
                    # Loop until joystick disconnects
                    while joystick.connected:
                        # Get joystick values from the left analogue stick
                        x_axis, y_axis = joystick['lx', 'ly']

                        # Get power from mixer function
                        power_left, power_right = mixer(yaw=x_axis, throttle=y_axis)

                        # Set motor speeds
                        set_speeds(power_left, power_right)

                        # Check for button presses since the last loop
                        presses = joystick.check_presses()
                        servo3 = 0
                        servo4 = 0.33

                        if joystick.presses.square:
                            print("Open Grabber")
                            servo3 = -1.0
                            UB.SetServoPosition3(servo3)

                        if joystick.presses.circle:
                            print("Close Grabber")
                            servo3 = -0.23
                            UB.SetServoPosition3(servo3)

                        if joystick.presses.cross:
                            print("Raise Grabber")
                            servo4 = 0.33
                            UB.SetServoPosition4(servo4)

                        if joystick.presses.triangle:
                            print("Lower Grabber")
                            servo4 = -0.10
                            UB.SetServoPosition4(servo4)

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
