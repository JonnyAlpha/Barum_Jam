# script to find the centroid (centre of mass) of an object of a specified colour
# prints the x and y coords of the centroid
# credits https://www.learnopencv.com/find-center-of-blob-centroid-using-opencv-cpp-python/

import cv2
import numpy as np

# capture the video frames
cap = cv2.VideoCapture(0)


# define the video capture frame size
cap.set(3, 640) # width
cap.set(4, 480) # height

while True:
    _, frame = cap.read()

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    # define range of colour to detect
    lower__blue = np.array([88, 131, 0], dtype=np.uint8)
    upper_blue = np.array([145, 255, 255], dtype=np.uint8)

    # setup the mask to detect only specified colour
    mask = cv2.inRange(hsv, lower__blue, upper_blue)


    ## convert image to grayscale image
    #gray_image = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    ## convert the mask image to binary image
    ret,thresh = cv2.threshold(mask,127,255,0)

    # calculate moments of binary image
    M = cv2.moments(thresh)

    area = M['m00']

    if (area > 3000000):


        # calculate x,y coordinate of center
        cX = int(M["m10"] / M["m00"])
        cY = int(M["m01"] / M["m00"])

        # put text and highlight the center
        cv2.circle(frame, (cX, cY), 5, (255, 0, 255), -1)
        cv2.putText(frame, "centroid", (cX - 25, cY - 25),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 255), 2)

        # print x coord, y coord, area
        print(cX, cY, area)
    elif (area < 3000000):
        print("nothing found yet")

    # display the image
    cv2.imshow("Object", frame)
    key = cv2.waitKey(1)
    if key==27:
        break

cv2.destroyAllWindows()
vidCapture.release()