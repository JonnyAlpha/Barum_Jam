#!/usr/bin/env python3
#
# Bespoke re-write for the Tidy up the Toys PiWars 2021 challenge
# Last updated:
# 23 Jan 20

# BUGS / ISSUES (Open):
# Need to try and move the distance() and position() functions out of the find_colour() function

# BUGS / ISSUES (Closed):
# Uses global variables throughout, now reduced by using return statements to read variable data into and out of functions
# Motor functions have been added but are very crude, the video output and program has become very laggy
# Crashes if it loses sight of the target - fixed by adding a try: except: excpetion handling 

# TO DO:
# Observer a principle of Don't Repeat Yourself (DRY).
#
# select_target() should be a generic target selection based on which part of the challenge is currently being tackled

# TO DO COMPLETED
# Condense the three find_color() into a single function(), using upper and lower HSV values set as variables
# Remove the if statements out of the main loop
# Need to move the Motor Driving into its own section and use variables to update the control
# Need to incorporate PID to the motor driving to illiminate errors
# Function Drive to Toy needs to be renamed driving and be fed variables so that it is generic, regardless of what section of the challenge

# EXPLANATION OF THE PROGRAM FLOW AND FUNCTION
# The first function called by main() is startup, this is where the motor controller and if used, the Pi Camera is set up.
# Next the main_loop() function is called, this starts the video capture and sets the image width and height based on the
# variables image_width and image_height.
# The program the enters a While loop that reads the first video frame, it then calls the select_target() function.
# The select_target() function looks at the list of toys to see which toys need to be collected, it selects the next available toy as the target
# Now back in the While loop, a series of if and elif conditional statement selects the appropriate OpenCV function,
# find_blue(), find_green(), find_red(), this is based on the target selected by select_target().
# From within these 'find_colour()' functions, distance() and position() are called, these functions determine the distance and position of the target
# Back in main_loop() the next function called is drive_to_toyl(), this uses the distance and position values stored in 'Z' and 'cx, cy, to determine which way to drive to the selected target
#
# When the target is close enough and in a central position in relation to the robot the drive_to_toy() function calls the pick_up_toy() function.
# pick_up_toy() function operates the grabber to pick up the toy
# May also check an IR sensor if fitted, to confirm that the toy is indeed within the jaws of the grabber.
#
# The position and steering information are written to the video frames using OpenCV and the frame is updated and displayed using cv2.imshow() in the main_loop().

# Driving functions have now been added to drive the robots motors
# The next progression will be to drive to the Drop Zone, once the toy is picked up. The Drop Zone will need to be identified by Arrows or an Accru Marker.
# Once in the 'Drop Zone', the toy will need to be dropped and then the next toy selected as a target.
# This should all be repeated until all all toys are delivered to the Drop Zone.

# import packages
import cv2
import numpy as np
from time import sleep
import ThunderBorg3

# declare GLOBAL constants (variable)
global TB #ThunderBorg
global Known_Distance
global Known_Width
global image_width
global image_height
global toys
global frame

# declare golbal variables
global driveLeft, driveRight
global toys_collected

# define variables
Known_Distance = 100 #100cm
Known_Width = 5 #5cm
image_width = 640
image_height = 480
toys = ["blue", "green", "red"]
target_toy = None  # allocates a none value
toys_collected = [] # allocates a null value to the list
#debugging = False #set to False to run in normal mode

# Setup the ThunderBorg Motor Driver board
TB = ThunderBorg3.ThunderBorg()
TB.Init()
if not TB.foundChip:
    boards = ThunderBorg3.ScanForThunderBorg()
    if len(boards) == 0:
        print('No ThunderBorg found, check you are attached :)')
    else:
        print('No ThunderBorg at address %02X, but we did find boards:' % (TB.i2cAddress))
        for board in boards:
            print("    %02X (%d) " % (board, board))
        print('If you need to change the Iï¿½C address change the setup line so it is correct, e.g.')
        print('TB.i2cAddress = 0x%02X' % (boards[0]))
    sys.exit()
# Ensure the communications failsafe has been enabled!
failsafe = False
for i in range(5):
    TB.SetCommsFailsafe(True)
    failsafe = TB.GetCommsFailsafe()
    if failsafe:
        break
if not failsafe:
    print('Board %02X failed to report in failsafe mode!' % (TB.i2cAddress))

def startup():
    print("Waiting for start command")
    # Check for controller
    # Check for start command - this will be a button press on the controller
    # Check external ultrasonic sensors if fitted to ensure safe to move - return distances
    # If not safe move to a safe position?
    # If safe to move carry out initial move (reverse, spin 180 degrees) to face the toys
    # move to start position, reverse and turn 180 degrees
    #TB.SetMotor1(-0.5)
    #TB.SetMotor2(-0.5)
    #sleep(0.5)
    #TB.SetMotor1(-0.5)
    #TB.SetMotor2(0.5)
    #sleep(0.5)

    # Return to main()

def start_position():
    print("Start Position")
    # will be used if we can identify a safe position to go to before searching for each toy
    # maybe a aruco marker insode the front wall

def select_target():
    # could be used to select any target dependent upon state?
    global toys
    #global target_toy
    #global toys_collected

    if len(toys)==0:
        print("No more toys to collect")
        target_toy = None
    else:
        for item in toys:

            if item == "blue":
                target_toy = "blue"
                print("Target selected =", target_toy)
                return target_toy

            elif item == "green":
                target_toy = "green"
                print("Target selected =", target_toy)
                return target_toy

            elif item == "red":
                target_toy = "red"
                print("Target selected =", target_toy)
                return target_toy

      #print("current target toy is")
      #print(target_toy)


def driving(): # movement
    print("Movement Control")

def grabber(): # grabber control
    print("Grabber Control")

# HSV COLOURSPACE START

def find_toy(frame, target_toy):

    # convert captured image to HSV colour space to detect colours
    toy = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)


    #cv2.imshow("toy", toy)
    #key = cv2.waitKey(0)

    if target_toy == "blue":
        print("searching for blue toy")
        #define range of colour to detect

        lower__hsv = np.array([88, 131, 0], dtype=np.uint8)
        upper_hsv = np.array([145, 255, 255], dtype=np.uint8)

    elif target_toy == "green":
        print("searching for green toy")
        #define range of colour to detect
        lower__hsv = np.array([33, 75, 0], dtype=np.uint8)
        upper_hsv = np.array([91, 255, 255], dtype=np.uint8)

    elif target_toy == "red":
        print("searching for red toy")
        # define range of colour to detect
        lower__hsv = np.array([156, 162, 0], dtype=np.uint8)
        upper_hsv = np.array([255, 255, 255], dtype=np.uint8)

    #setup the mask to detect only specified colour
    mask = cv2.inRange(toy, lower__hsv, upper_hsv)


    #cv2.imshow("mask", mask)
    #key = cv2.waitKey(0)

    # setup the results to display
    colour_res = cv2.bitwise_and(frame, frame, mask=mask)
    #colour_res = cv2.bitwise_and(frame, frame, mask=mask)

    # detect the contours of the shapes and keep the largest
    contours, hierarchy  = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    #was_, blue_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(contours), contours) for contours in contours]

    if len(contour_sizes) > 0:
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # draw a green bounding box around the detected object
        x, y, w, h = cv2.boundingRect(biggest_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #print(w, h)

        # HSV COLOURSPACE END
        mask = mask # allocates variable mask with data from blue_mask to be passed to position function


        #distance(w, frame) # calls distance function and passes 'w' and 'frame'
        #position(mask, frame) # calls position function and passes 'mask' and 'frame'

        #show frames
        #show mask

        Z = distance(w, frame)
        cx, cy = position(mask, frame)

        print("we got here")
        print("Z = ", Z)
        print("cx, cy = ", cx, cy)
        return cx, cy, Z

def distance(w, frame):
    #global Z
    print("distance, z") #Debugging
    # DISTANCE (z) BEGIN

    # initialise the known distance from the camera to the object which is 300mm 11.81102 inches
    KNOWN_DISTANCE = 100
    Z = KNOWN_DISTANCE
    # initialise the know object width, which is 50mm or 1.968504 inches
    KNOWN_WIDTH = 0.5
    D = KNOWN_WIDTH
    # d = width in pixels at 100cm = 30 - recheck if camera position changes
    d = 30

    f = d*Z/D #f = focallength

    d = w # w is the perceived width in pixels calculated by OpenCV Contours

    Z = D*f/d
    print("pixel width =", w)

    cv2.putText(frame, "%.1fcm" % (Z), (frame.shape[1] - 400, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    # %.1f = 1 decimal point, px = px
    # adds the variable w - width to the screen
    return Z

    # DISTANCE (z) END

def position(mask, frame):
    #global cx
    #global cy
    print("position x, y")

    # POSITION (x, y) BEGIN

    # convert image to binary
    ret, thresh = cv2.threshold(mask, 127,255,0)

    # calculate moments of the binary image
    M = cv2.moments(thresh)

    # calculate the x, y coordinates of the centre

    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # put text and highlight the centre
    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    cv2.putText(frame, "centroid", (cx - 25, cy - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

    return cx, cy

    # POSITION (x, y) END

def drive_to_toy(frame, target_toy, cx, cy, Z):

    #global target_toy
    #global toys_collected

    print("Driving to toy")
    print("Distance = ", Z)
    print("Position (x, y) = ", cx, cy)
    drive = ""
    # check distance to target
    if Z >= 30:
        print("Navigating to target")
        # insert driving forward
        if cx > 320:
            print("steering left")
            drive = "steering left"
            #Enter motor controls here
            #TB.SetMotor1(0.25)
            #TB.SetMotor2(0.5)
            driveLeft = 0.25
            driveRight = 0.50
            cv2.putText(frame, drive, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.putText(frame, "%.1fpx" % (cx), (frame.shape[1] - 200, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            return driveLeft, driveRight

        elif cx < 320:
            print("steering right")
            drive = "steering right"
            # Enter motor controls here
            #TB.SetMotor1(0.5)
            #TB.SetMotor2(0.25)
            driveLeft = 0.50
            driveRight = 0.25
            cv2.putText(frame, drive, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.putText(frame, "%.1fpx" % (cx), (frame.shape[1] - 200, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            return driveLeft, driveRight

        else:
            print("straight ahead")
            drive = "straight ahead"
            # Enter motor controls here
            #TB.SetMotor1(0.5)
            #TB.SetMotor2(0.5)
            driveLeft = 0.50
            driveRight = 0.50
            cv2.putText(frame, drive, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            cv2.putText(frame, "%.1fpx" % (cx), (frame.shape[1] - 200, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
            return driveLeft, driveRight

    else: #was elif Z <= 29:
        print("target in range")
        drive = "target in range"
        driveLeft = 0
        driveRight = 0
        cv2.putText(frame, drive, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        #cv2.putText(frame, "%.1fpx" % (cx), (frame.shape[1] - 200, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)
        return driveLeft, driveRight

    #if cx > 300 and cx < 340:
    #    TB.SetMotor1(0)
    #    TB.SetMotor2(0)
    #    driveLeft = 0
    #    driveRight = 0

    #        pick_up_toy(target_toy, toys_collected)

    #cv2.putText(frame, drive, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    #cv2.putText(frame, "%.1fcm" % (cx), (frame.shape[1] - 400, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    #return driveLeft, driveRight

def search_mode():
    driveLeft = 0.5
    sleep(1)
    driveRight = 0.5
    sleep(1)

def pick_up_toy(target_toy, toys_collected):
    print("Picking up toy")
    sleep(2)
    print(target_toy) # test to see if target_toy contains a value?
    toys_collected.append(target_toy)
    toys.remove(target_toy)
    print("Toys collected so far", toys_collected)
    if not toys:
        print("All toys picked up")
        target_toy = None
    else:
        print("Toys remaining", toys)
        find_drop_zone()
    sleep(2)

def find_drop_zone():
    print("Searching for Drop Zone")
    # Need OpenCV code here to find Drop Zone markers, poss two Arrows
    # Insert Acuro Marker finding routine here, probably start by reversing and turning left, to face the Drop Zone

def put_down_toy():
    print("Put down toy")

def drive_motors(driveLeft, driveRight):
    TB.SetMotor1(driveLeft)
    TB.SetMotor2(driveRight)

def main_loop():

    # capture the video frames (0) = first camera
    cap = cv2.VideoCapture(0)

    # define the video capture frame size
    cap.set(3, image_width) # set as a global variable
    cap.set(4, image_height) # set as a global variable

    while True:
        # check toys list
            # if no toys left check toys_collected
                # if all toys collected finish?
            # if toys left
                # collect toys

        _, frame = cap.read()
        frame = cv2.flip(frame, 0) #flips the video 180 degrees

        #cv2.imshow("frame", frame) # For debugging
        #key = cv2.waitKey(0) # For debugging

        target_toy = select_target()
        #select_target() # this could be starting position, toys, or drop zone based on what stage of the challenge we are at
        try:
            if target_toy:

                cx, cy, Z = find_toy(frame, target_toy)
                #print("Z = ", Z) # For debugging
                #print("cx, cy = ", cx, cy) # For debugging


                #cv2.imshow("frame", frame) # For debugging
                #key = cv2.waitKey(0) # For debugging

                driveLeft, driveRight = drive_to_toy(frame, target_toy, cx, cy, Z)
                #if cx > 300 and cx < 340:
                #    #TB.SetMotor1(0)
                #    #TB.SetMotor2(0)
                #    driveLeft = 0
                #    driveRight = 0
                #    pick_up_toy(target_toy, toys_collected)


                drive_motors(driveLeft, driveRight)

            else:
                print("No target toy")
                print("May need to give up here, or enter search mode")
                search_mode()

                break

        except:
            print("nothing found")

        # output the results in windows
        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    TB.MotorsOff()
    TB.SetCommsFailsafe(False)
    TB.SetLedShowBattery(False)
    TB.SetLeds(0,0,0)

def main():
    startup() # set everything up and check starting status and surroundings
    start_position() # move to start position if we set one

    # if we are ok and have been told to start do the main loop
    #main_loop(driveLeft, driveRight)
    main_loop()

main()


