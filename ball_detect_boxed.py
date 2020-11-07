# script for 'tidy up the toys' a PiWars2021 challenge
# detects a coloured ball and draws a bounding box around it
# use multicolour_detect.py to establish hsv numbers for each colour

# import the neccessary packages
import cv2
import numpy as np

# capture the video frames (0) = first camera
cap = cv2.VideoCapture(0)


# define the video capture frame size
cap.set(3, 640) # width
cap.set(4, 480) # height

while True:
    _, frame = cap.read()

    # HSV COLOURSPACE START
    # convert captured image to HSV colour space to detect colours
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define range of colour to detect
    lower__blue = np.array([88, 131, 0], dtype=np.uint8)
    upper_blue = np.array([145, 255, 255], dtype=np.uint8)
    # insert red and green

    #setup the mask to detect only specified colour
    blue_mask = cv2.inRange(hsv, lower__blue, upper_blue)
    # insert red and green

    # HSV COLOURSPACE END

    # CONTOURS START

    # detect the contours of the shapes
    blue_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    # insert red and green

    contour_sizes = [(cv2.contourArea(blue_contours), blue_contours) for blue_contours in blue_contours]
    biggest_blue_contour = max(contour_sizes, key=lambda x: x[0])[1]
    # insert red and green

    # draw a rectangle around the detected object
    x, y, w, h = cv2.boundingRect(biggest_blue_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # insert red and green

    # DISPLAY

    # setup the results to display
    blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)


    # output the results in windows
    cv2.imshow("frame", frame)
    cv2.imshow("mask", blue_mask)
    cv2.imshow("blue_res", blue_res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()
