#!/usr/bin/env python3
# coding: Latin
# second attempt at incorporating MonsterBorg driving and my object detection

# Load library functions we want
import numpy as np
import cv2
import sys
import ThunderBorg3 #for python3
import time
import threading
import picamera
import picamera.array

#GLobal variables
global TB
#global cap #not required
global colour
global image
global camera
global running

running = True
debug = False
colour = "blue" #set the target colour (this will be expanded into a target selection sequence for all three colours)

# Setup the ThunderBorg
TB = ThunderBorg3.ThunderBorg()
# TB.i2cAddress = 0x15                  # Uncomment and change the value if you have changed the board address
TB.Init()
if not TB.foundChip:
    boards = ThunderBorg.ScanForThunderBorg()
    if len(boards) == 0:
        print("No ThunderBorg found, check you are attached :)")
    else:
        print("No ThunderBorg at address %02X, but we did find boards:" % (TB.i2cAddress))
        for board in boards:
            print("    %02X (%d)" % (board, board))
        print("If you need to change the IÃÂ²C address change the setup line so it is correct, e.g.")
        print("TB.i2cAddress = 0x%02X" % (boards[0]))
    sys.exit()
TB.SetCommsFailsafe(False)

# Power settings
voltageIn = 14.6                        # Total battery voltage to the ThunderBorg
voltageOut = 14.6 * 0.95                # Maximum motor voltage, we limit it to 95% to allow the RPi to get uninterrupted power

# Camera settings
imageWidth = 640  # Camera image width
imageHeight = 480  # Camera image height
frameRate = 3  # Camera image capture frame rate

# Auto drive settings
autoMaxPower = 1.0  # Maximum output in automatic mode
autoMinPower = 0.2  # Minimum output in automatic mode
autoMinArea = 10  # Smallest target to move towards
autoMaxArea = 10000  # Largest target to move towards
autoFullSpeedArea = 300  # Target size at which we use the maximum allowed output


# Setup the power limits
if voltageOut > voltageIn:
    maxPower = 1.0
else:
    maxPower = voltageOut / float(voltageIn)
autoMaxPower *= maxPower

# Image stream processing thread
class StreamProcessor(threading.Thread):
    def __init__(self):
        super(StreamProcessor, self).__init__()
        self.stream = picamera.array.PiRGBArray(camera)
        self.event = threading.Event()
        self.terminated = False
        self.start()
        self.begin = 0

    def run(self):
        # This method runs in a separate thread
        while not self.terminated:
            # Wait for an image to be written to the stream
            if self.event.wait(1):
                try:
                    # Read the image and do some processing on it
                    self.stream.seek(0)
                    self.ProcessImage(self.stream.array, colour)
                finally:
                    # Reset the stream and event
                    self.stream.seek(0)
                    self.stream.truncate()
                    self.event.clear()

    # Image processing function
    def ProcessImage(self, image, colour):
        if debug:
            # View the original image seen by the camera.
            cv2.imshow("original", image)
            cv2.waitKey(0)

        # Blur the image
        blur = cv2.medianBlur(image, 5)
        if debug:
            cv2.imshow('blur', blur)
            cv2.waitKey(0)

        # convert captured image to HSV colour space to detect colours
        hsv = cv2.cvtColor(blur, cv2.COLOR_BGR2HSV)
        if debug:
            # View the converted image seen by the camera.
            cv2.imshow('hsv', hsv)
            cv2.waitKey(0)

        # extract the 'Hue', or colour, from the image. The 'inRange'
        # method will extract the colour we are interested in (between 0 and 180)
        # In testing, the Hue value for red is between 95 and 125
        # Green is between 50 and 75
        # Blue is between 20 and 35
        # Yellow is... to be found!


        if colour == "red":

            print("searching red")
            #imrange = cv2.inRange(image, numpy.array((95, 127, 64)), numpy.array((125, 255, 255)))


        elif colour == "green":

            print("searching green")
            #imrange = cv2.inRange(image, numpy.array((50, 127, 64)), numpy.array((75, 255, 255)))

        elif colour == 'blue':
            #define range of colour to detect
            lower__blue = np.array([88, 131, 0], dtype=np.uint8)
            upper_blue = np.array([145, 255, 255], dtype=np.uint8)

            #setup the mask to detect only specified colour
            blue_mask = cv2.inRange(hsv, lower__blue, upper_blue)

            # setup the results to display (not used)
            blue_res = cv2.bitwise_and(hsv, hsv, mask=blue_mask)

            # set the variable imrange to the results of the blue object detection routine
            imrange = blue_mask

            #imrange = cv2.inRange(image, numpy.array((20, 64, 64)), numpy.array((35, 255, 255)))

        # I used the following code to find the approximate 'hue' of the ball in
        # front of the camera
        #        for crange in range(0,170,10):
        #            imrange = cv2.inRange(image, numpy.array((crange, 64, 64)), numpy.array((crange+10, 255, 255)))
        #            print(crange)
        #            cv2.imshow('range',imrange)
        #            cv2.waitKey(0)

        # View the filtered image found by 'imrange'
        if debug:
            cv2.imshow('imrange', imrange)
            cv2.waitKey(0)

        # detect the contours of the shapes
        contours, hierarchy  = cv2.findContours(imrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #_, contours, hierarchy  = cv2.findContours(imrange, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        #if debug:
        #    cv2.imshow('contours', contours)
        #    cv2.waitKey(0)

        # keep the largest contours
        contour_sizes = [(cv2.contourArea(contours), contours) for contours in contours]
        biggest_contour = max(contour_sizes, key=lambda x: x[0])[1]

        # draw a green bounding box around the detected object
        x, y, w, h = cv2.boundingRect(biggest_contour)
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)

        # initialise the known distance from the camera to the object which is 300mm 11.81102 inches
        KNOWN_DISTANCE = 100
        Z = KNOWN_DISTANCE
        # initialise the know object width, which is 50mm or 1.968504 inches
        KNOWN_WIDTH = 0.5
        D = KNOWN_WIDTH
        # d = width in pixels at 100cm = 30 - recheck if camera position changes
        d = 30

        f = d*Z/D #f = focallength

        d = w # w is the perceieved width in pixels calculated by OpenCV Contours

        Z = D*f/d
        #print("pixel width =", w)

        cv2.putText(image, "%.1fcm" % (Z), (image.shape[1] - 400, image.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
        # %.1f = 1 decimal point, px = px
        # adds the variable w - width to the screen

        # POSITION (x, y) BEGIN

        # convert image to binary
        ret, thresh = cv2.threshold(imrange, 127,255,0)

        # calculate moments of the binary image
        M = cv2.moments(thresh)

        # calculate the x, y coordinates of the centre
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])

        # put text and highlight the centre
        cv2.circle(image, (cx, cy), 5, (255, 255, 255), -1)
        cv2.putText(image, "centroid", (cx - 25, cy - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

        cv2.imshow("image", image)
        cv2.waitKey(1)
        # Go through each contour
        # using area to determine if ball is seen or not
        foundArea = -1
        foundX = -1
        foundY = -1
        for contour in contours:
            x, y, w, h = cv2.boundingRect(biggest_contour)
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cx = x + (w / 2)
            cy = y + (h / 2)
            area = w * h
            if foundArea < area:
                foundArea = area
                foundX = cx
                foundY = cy
        if foundArea > 0:
            ball = [foundX, foundY, foundArea]
        else:
            ball = None
        # Set drives or report ball status
        self.SetSpeedFromBall(ball)

    # Set the motor speed from the ball position
    def SetSpeedFromBall(self, ball):
        global TB
        driveLeft = 0.0
        driveRight = 0.0
        if ball:
            x = ball[0]
            area = ball[2]
            if area < autoMinArea:
                print('Too small / far')
            elif area > autoMaxArea:
                print('Close enough')
            else:
                if area < autoFullSpeedArea:
                    speed = 1.0
                else:
                    speed = 1.0 / (area / autoFullSpeedArea)
                speed *= autoMaxPower - autoMinPower
                speed += autoMinPower
                direction = (x - imageCentreX) / imageCentreX
                if direction < 0.0:
                    # Turn right
                    print('Turn Right')
                    driveLeft = speed
                    driveRight = speed * (1.0 + direction)
                else:
                    # Turn left
                    print('Turn Left')
                    driveLeft = speed * (1.0 - direction)
                    driveRight = speed
                print('%.2f, %.2f' % (driveLeft, driveRight))
        else:
            print('No ball')

        TB.SetMotor1(driveLeft)
        TB.SetMotor2(driveRight)

# Image capture thread
class ImageCapture(threading.Thread):
    def __init__(self):
        super(ImageCapture, self).__init__()
        self.start()

    def run(self):
        global camera
        global processor
        print('Start the stream using the video port')
        camera.capture_sequence(self.TriggerStream(), format='bgr', use_video_port=True)
        print('Terminating camera processing...')
        processor.terminated = True
        processor.join()
        print('Processing terminated.')

    # Stream delegation loop
    def TriggerStream(self):
        global running
        while running:
            if processor.event.is_set():
                time.sleep(0.01)
            else:
                yield processor.stream
                processor.event.set()

# Startup sequence
print('Setup camera')

# setup the camera, (0) = first camera
camera = picamera.PiCamera()

# define the video capture frame size
camera.resolution = (imageWidth, imageHeight)
camera.framerate = frameRate

imageCentreX = imageWidth / 2.0
imageCentreY = imageHeight / 2.0

print("Setup the stream processing thread")
processor = StreamProcessor()

print("Wait ...")
time.sleep(2)
captureThread = ImageCapture()

try:
    print("Press CTRL+C to quit")
    TB.MotorsOff()
    TB.SetLedShowBattery(True)
    # Loop indefinitely until we are no longer running
    while running:
        # Wait for the interval period
        # You could have the code do other work in here :)
        time.sleep(1.0)
        # Disable all drives
    TB.MotorsOff()
except KeyboardInterrupt:
    # CTRL+C exit, disable all drives
    print("\nUser shutdown")
    TB.MotorsOff()
except:
    # Unexpected error, shut down!
    e = sys.exc_info()[0]
    print
    print(e)
    print("\nUnexpected error, shutting down!")
    TB.MotorsOff()

# Tell each thread to stop, and wait for them to end
running = False
captureThread.join()
processor.terminated = True
processor.join()
del camera
TB.MotorsOff()
TB.SetLedShowBattery(False)
TB.SetLeds(0,0,0)
print("Program terminated.")
