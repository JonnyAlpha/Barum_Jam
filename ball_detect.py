# script to detect blue, green and red coloured balls using OpenCV HSV colour space
# draws around the contours of the identified shapes
# credits: https://www.youtube.com/watch?v=3D7O_kZi8-o
# use multicolour_detect.py to establish hsv numbers for each colour

import cv2
import numpy as np

# capture the video frames
cap = cv2.VideoCapture(0);

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define the hsv values
    # blue
    l_blue = [88, 131, 0]
    u_blue = [145, 255, 255]
    l_b = np.array(l_blue)
    u_b = np.array(u_blue)

    # green
    l_green = [33, 75, 0]
    u_green = [91, 255, 255]
    l_g = np.array([l_green])
    u_g = np.array([u_green])

    # red
    l_red = [156, 162, 0]
    u_red = [255, 255, 255]
    l_r = np.array([l_red])
    u_r = np.array([u_red])

    #setup the three colour masks
    blue_mask = cv2.inRange(hsv, l_b, u_b)
    green_mask = cv2.inRange(hsv, l_g, u_g)
    red_mask = cv2.inRange(hsv, l_r, u_r)

    # detect the contours of the shapes
    blue_contours, hierarchy = cv2.findContours(blue_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    green_contours, hierarchy = cv2.findContours(green_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    red_contours, hierarchy = cv2.findContours(red_mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # draw around the countours of the detected shapes
    for cnt in blue_contours:
        area = cv2.contourArea(cnt) # write the size of the contours to area
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 5)
    for cnt in green_contours:
        area = cv2.contourArea(cnt) # write the size of the contours to area
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(frame, [approx], 0, (255, 255, 0), 5)
    for cnt in red_contours:
        area = cv2.contourArea(cnt) # write the size of the contours to area
        approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        cv2.drawContours(frame, [approx], 0, (255, 0, 255), 5)

    # setup the results to display
    blue_res = cv2.bitwise_and(frame, frame, mask=blue_mask)
    green_res = cv2.bitwise_and(frame, frame, mask=green_mask)
    red_res = cv2.bitwise_and(frame, frame, mask=red_mask)

    # output the results in windows
    cv2.imshow("frame", frame)
    #cv2.imshow("mask", mask)
    #cv2.imshow("blue_res", blue_res)
    #cv2.imshow("green_res", green_res)
    #cv2.imshow("red_res", red_res)

    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()

