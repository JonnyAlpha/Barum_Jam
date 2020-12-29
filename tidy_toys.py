#!/usr/bin/env python3
# 29Dec20 2020 Re-Work of attempt at complete re-write of working program for the Tidy up the Toys PiWars 2021 challenge

# BUGS / ISSUES:
# Uses global variables throughout, need to switch to classes
# Program finds and in theoary picks ups all toys, but when last toy has been collected
# it continues to search for the last target toy? - FIxed

# To Do:
# Need to add error checking if nothing seen - completed
# Need to try and move the distance() and position() functions out of each of the find_colour() functions to follow the
# principle of Don't Repeat Yourself (DRY).
# Condense the three find_color() into a single function(), using upper and lower HSV values set as variables

# Explanation of the function / program flow:
# The first function called by main() is startup, this is where the motor controller and if used, the Pi Camera is set up.
# Next the main_loop() function is called, this starts the video capture and sets the image width and height based on the
# variables image_width and image_height.
# The program the enters a While loop that reads the first video frame, it then calls the select_target() function.
# The select_target() function looks at the list of toys to see which toys need to be collected, it selects the next available toy as the target
# Now back in the WHile loop, a series of if and elif conditional statements and selects appropriate OpenCV function,
# find_blue(), find_green(), find_red(), based on the target selected by select_target().
# From within these 'find_colour()' functions, distance() and position() are called, these functions determine the distance and positoon of the target
# Back in main_loop() drive_to_toyl()uses the distance and position values stored in 'Z' and 'cx, cy, to determine which way to drive to the selected target
# When the target is close enough and central drive_to_toy() calls the pick_up_toy() function. This will operate the grabber (but may also chec an IR sensor
# if we install one to confirm that the toy is indeed within the jaws of the grabber.
# The position and steering information are written to the video frames using OpenCV and the fram is updated using cv2.imshow() in the main_loop().

# The next progression will be to drive to the Drop Zone, once the toy is picked up. The Drop Zone will need to be identified by Arrows or an Accru Marker.
# Once in the 'Drop Zone', the toy will need to be dropped and then the next toy selected as a target.
# This should all be repeated until all all toys are delivered to the Drop Zone.

# import packages
import cv2
import numpy as np
from time import sleep

# declare GLOBAL variable
global TB #ThunderBorg
global Known_Distance
global Known_Width
global image_width
global image_height
global toys
global target_toy
global toys_collected
global frame
global Z
global cx, cy

# define variables
Known_Distance = 100 #100cm
Known_Width = 5 #5cm
image_width = 640
image_height = 480
toys = ["blue", "green", "red"]
target_toy = None  # allocates a none value
toys_collected = [] # allocates a null value to the list

def startup():
    print("Starting up")

def select_target():
    global toys
    global target_toy
    global toys_collected

    for item in toys:

        if item == "blue":
            target_toy = "blue"
            print("Target selected =", target_toy)
            break

        elif item == "green":
            target_toy = "green"
            print("Target selected =", target_toy)
            break

        elif item == "red":
            target_toy = "red"
            print("Target selected =", target_toy)
            break

    if len(toys)==0:
        print("No more toys to collect")
        target_toy = None
    else:
        print("current target toy is")
        print(target_toy)

    sleep(0.25)

def driving(): # movement
    print("Movement Control")

def grabber(): # grabber control
    print("Grabber Control")

# HSV COLOURSPACE START
def find_blue(frame):
    print("Searching for Blue Box")
    # convert captured image to HSV colour space to detect colours
    blue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define range of colour to detect
    lower__blue = np.array([88, 131, 0], dtype=np.uint8)
    upper_blue = np.array([145, 255, 255], dtype=np.uint8)

    #setup the mask to detect only specified colour
    blue_mask = cv2.inRange(blue, lower__blue, upper_blue)

    # setup the results to display
    blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # detect the contours of the shapes and keep the largest
    blue_contours, hierarchy  = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #was_, blue_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(blue_contours), blue_contours) for blue_contours in blue_contours]

    if len(contour_sizes) > 0:
        biggest_blue_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # draw a green bounding box around the detected object
        x, y, w, h = cv2.boundingRect(biggest_blue_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #print(w, h)

        # HSV COLOURSPACE END
        mask = blue_mask # allocates variable mask with data from blue_mask to be passed to position function

        distance(w, frame) # calls distance function and passes 'w' and 'frame'
        position(mask, frame) # calls position function and passes 'mask' and 'frame'

def find_green(frame):
    print("Searching for Green Box")
    # convert captured image to HSV colour space to detect colours
    green = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of colour to detect
    lower__green = np.array([33, 75, 0], dtype=np.uint8)
    upper_green = np.array([91, 255, 255], dtype=np.uint8)

    # setup the mask to detect only specified colour
    green_mask = cv2.inRange(green, lower__green, upper_green)

    # setup the results to display
    green_res = cv2.bitwise_and(frame, frame, mask=green_mask)

    # detect the contours of the shapes and keep the largest
    green_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # was_, green_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(green_contours), green_contours) for green_contours in green_contours]

    if len(contour_sizes) > 0:
        biggest_green_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # draw a green bounding box around the detected object
        x, y, w, h = cv2.boundingRect(biggest_green_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # print(w, h)

        # HSV COLOURSPACE END
        mask = green_mask  # allocates variable mask with data from green_mask to be passed to position function

        distance(w, frame)  # calls distance function and passes 'w' and 'frame'
        position(mask, frame)  # calls position function and passes 'mask' and 'frame'

def find_red(frame):
    print("Finding Red Box")
    # convert captured image to HSV colour space to detect colours
    red = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of colour to detect
    lower__red = np.array([156, 162, 0], dtype=np.uint8)
    upper_red = np.array([255, 255, 255], dtype=np.uint8)

    # setup the mask to detect only specified colour
    red_mask = cv2.inRange(red, lower__red, upper_red)

    # setup the results to display
    red_res = cv2.bitwise_and(frame, frame, mask=red_mask)

    # detect the contours of the shapes and keep the largest
    red_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # was_, red_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(red_contours), red_contours) for red_contours in red_contours]

    if len(contour_sizes) > 0:
        biggest_red_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # draw a green bounding box around the detected object
        x, y, w, h = cv2.boundingRect(biggest_red_contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # print(w, h)

        # HSV COLOURSPACE END
        mask = red_mask  # allocates variable mask with data from red_mask to be passed to position function

        distance(w, frame)  # calls distance function and passes 'w' and 'frame'
        position(mask, frame)  # calls position function and passes 'mask' and 'frame'

def distance(w, frame):
    global Z
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


    cv2.putText(frame, "%.1fcm" % (Z), (frame.shape[1] - 400, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    # %.1f = 1 decimal point, px = px
    # adds the variable w - width to the screen

    # DISTANCE (z) END

def position(mask, frame):
    global cx
    global cy
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

    # POSITION (x, y) END

def find_drop_zone():
    print("Find Drop Zone")

def drive_to_toy(frame, target_toy):
    #global target_toy
    #global toys_collected

    print("Driving to toy")
    print("Distance = ", Z)
    print("Position (x, y) = ", cx, cy)
    drive = ""
    # check distance to target
    if Z > 10:
        print("Navigating to target")
        # insert driving forward
        if cx > 320:
            print("steer left")
            drive = "steer left"
            #Enter motor controls here
        elif cx < 320:
            print("steer right")
            drive = "steer right"
            # Enter motor controls here
        else:
            print("straight ahead")
            drive = "straight ahead"
            # Enter motor controls here
    elif Z < 10:
        print("target in range")
        drive = "target in range"

        if cx > 290 and cx < 350:
            pick_up_toy(target_toy, toys_collected)

    cv2.putText(frame, drive, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

def pick_up_toy(target_toy, toys_collected):
    #global toys_collected
    #global target_toy
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
    sleep(2)

def put_down_toy():
    print("Put down toy")

def main_loop():
    global toys_collected
    global target_toy
    # capture the video frames (0) = first camera
    cap = cv2.VideoCapture(0)

    # define the video capture frame size
    cap.set(3, image_width) # set as a global variable
    cap.set(4, image_height) # set as a global variable

    #target_toy = random.choice(toys)
    #print("Random first toy selected is:", target_toy)
    #sleep(2)
    while True:
        #print("Toys collected so far:", toys_collected)
        #sleep(0.25)

        _, frame = cap.read()

        select_target()

        if target_toy == "blue":
            find_blue(frame)

        elif target_toy == "green":
            find_green(frame)

        elif target_toy == "red":
            find_red(frame)

        elif target_toy == None:
            print("No target toy")
            print("May need to exit here?")
            break

        if target_toy:
            drive_to_toy(frame, target_toy)

        else:
            break
        # output the results in windows

        cv2.imshow("frame", frame)

        key = cv2.waitKey(1)
        if key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

def main():
    startup()
    main_loop()

main()
