# finding the (x, y) position and (z) distance of an object of known size
# use multicolour_detect.py to establish hsv numbers for each colour
# using a blue ball of 50mm diameter
# Uses triangular similarity to calculate (z) distance
# Uses OpenCv Moments to calculate (x,y) position

import numpy as np
import cv2

def main():
    # capture the video frames (0) = first camera
    cap = cv2.VideoCapture(0)

    # define the video capture frame size, keeps it low res to save CPU
    cap.set(3, 640) # width
    cap.set(4, 480) # height

    while True:
        _, frame = cap.read()
        frame = cv2.flip(frame, 0)
        find_blue(frame)
        #find_red(frame)
        #find_green(frame)

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

    # detect the contours of the shapes and keep the largest
    _, blue_contours, hierarchy  = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    #_, blue_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    contour_sizes = [(cv2.contourArea(blue_contours), blue_contours) for blue_contours in blue_contours]
    biggest_blue_contour = max(contour_sizes, key=lambda x: x[0])[1]

    # draw a green bounding box around the detected object
    x, y, w, h = cv2.boundingRect(biggest_blue_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    #print(w, h)

    # HSV COLOURSPACE END

    # DISTANCE BEGIN

    # initialise the known distance from the camera to the object which is 100cm 
    KNOWN_DISTANCE = 100
    Z = KNOWN_DISTANCE
    # initialise the know object width, which is 0.5cm
    KNOWN_WIDTH = 0.5
    D = KNOWN_WIDTH
    # d = width in pixels at 100cm = 30 - recheck if camera position changes
    d = 30

    f = d*Z/D #f = focallength

    d = w # w is the perceieved width in pixels calculated by OpenCV Contours

    Z = D*f/d
    print(w, "px")

    cv2.putText(frame, "%.1fcm" % (Z), (frame.shape[1] - 400, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

    # %.1f = 1 decimal point, cm = unit of measurement to be displayed
    # adds the variable w - width to the screen

    # POSITION (x, y) BEGIN

    # convert image to binary
    ret, thresh = cv2.threshold(blue_mask, 127,255,0)

    # calculate moments of the binary image
    M = cv2.moments(thresh)

    # calculate the x, y coordinates of the centre
    cx = int(M["m10"] / M["m00"])
    cy = int(M["m01"] / M["m00"])

    # put text and highlight the centre
    cv2.circle(frame, (cx, cy), 5, (255, 255, 255), -1)
    cv2.putText(frame, "centroid", (cx - 25, cy - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)


    #cv2.imshow("mask", blue_mask)
    #cv2.imshow("blue_res", blue_res)

main()
cap.release()
cv2.destroyAllWindows()
