# second draft of script for 'tidy up the toys' a PiWars2021 challenge
# detects a blue, red and green object and draws a green bouding box around it
# use multicolour_detect.py to establish hsv numbers for each colour

# import the neccessary packages
import cv2
import numpy as np


def main():
    # capture the video frames (0) = first camera
    cap = cv2.VideoCapture(0)

    # define the video capture frame size
    cap.set(3, 640) # width
    cap.set(4, 480) # height

    while True:
        _, frame = cap.read()
        find_blue(frame)
        find_red(frame)
        find_green(frame)
        # output the results in windows
        cv2.imshow("frame", frame)


        key = cv2.waitKey(1)
        if key == 27:
            break

# HSV COLOURSPACE START
def find_blue(frame):
    # convert captured image to HSV colour space to detect colours
    blue = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    #define range of colour to detect
    lower__blue = np.array([88, 131, 0], dtype=np.uint8)
    upper_blue = np.array([145, 255, 255], dtype=np.uint8)

    #setup the mask to detect only specified colour
    blue_mask = cv2.inRange(blue, lower__blue, upper_blue)

    # setup the results to display
    blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)

    # detect the contours of the shapes
    blue_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(blue_contours), blue_contours) for blue_contours in blue_contours]
    biggest_blue_contour = max(contour_sizes, key=lambda x: x[0])[1]

    # draw a green bounding box around the detected object
    x, y, w, h = cv2.boundingRect(biggest_blue_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # display results
    cv2.imshow("mask", blue_mask)
    cv2.imshow("blue_res", blue_res)

def find_red(frame):
    # convert captured image to HSV colour space to detect colours
    red = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of colour to detect
    lower__red = np.array([156,162, 0], dtype=np.uint8)
    upper_red = np.array([255, 255, 255], dtype=np.uint8)

    # setup the mask to detect only specified colour
    red_mask = cv2.inRange(red, lower__red, upper_red)

    # setup the results to display
    red_res = cv2.bitwise_and(frame, frame, mask=red_mask)

    # detect the contours of the shapes
    red_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(red_contours), red_contours) for red_contours in red_contours]
    biggest_red_contour = max(contour_sizes, key=lambda x: x[0])[1]

    # draw a green bounding box around the detected object
    x, y, w, h = cv2.boundingRect(biggest_red_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # display results
    cv2.imshow("mask", red_mask)
    cv2.imshow("red_res", red_res)

def find_green(frame):
    # convert captured image to HSV colour space to detect colours
    green = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of colour to detect
    lower__green = np.array([33, 75, 0], dtype=np.uint8)
    upper_green = np.array([91, 255, 255], dtype=np.uint8)

    # setup the mask to detect only specified colour
    green_mask = cv2.inRange(green, lower__green, upper_green)

    # setup the results to display
    green_res = cv2.bitwise_and(frame, frame, mask=green_mask)

    # detect the contours of the shapes
    green_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(green_contours), green_contours) for green_contours in green_contours]
    biggest_green_contour = max(contour_sizes, key=lambda x: x[0])[1]

    # draw a green bounding box around the detected object
    x, y, w, h = cv2.boundingRect(biggest_green_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

    # display the results
    cv2.imshow("mask", green_mask)
    cv2.imshow("green_res", green_res)

    # HSV COLOURSPACE END

main()
cap.release()
cv2.destroyAllWindows()
