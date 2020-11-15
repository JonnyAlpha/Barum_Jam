# finding the distance of an object of known size
# use multicolour_detect.py to establish hsv numbers for each colour
# using a blue ball of 50mm diameter

import numpy as np
import cv2

def main():
    # capture the video frames (0) = first camera
    cap = cv2.VideoCapture(0)


    # define the video capture frame size
    cap.set(3, 640) # width
    cap.set(4, 480) # height

    while True:
        _, frame = cap.read()
        find_blue(frame)
        #find_red(frame)
        #find_green(frame)

        # distance
        # initialise the known distance from the camera to the object which is 300mm 11.81102 inches
        KNOWN_DISTANCE = 100

        # initialise the know object width, which is 50mm or 1.968504 inches
        KNOWN_WIDTH = 0.5

        # read the first frames to find

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
    contour_sizes = [(cv2.contourArea(blue_contours), blue_contours) for blue_contours in blue_contours]
    biggest_blue_contour = max(contour_sizes, key=lambda x: x[0])[1]

    # draw a green bounding box around the detected object
    x, y, w, h = cv2.boundingRect(biggest_blue_contour)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(w, h) # debugging - prints the variable w - width and h - height to the terminal
    
    cv2.putText(frame, "%.1fpx" % (w), (frame.shape[1] - 400, frame.shape[0] - 100), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)
    # %.1f = 1 decimal point, px = px
    # adds the variable w - width to the screen 
    # was cv2.putText(frame, "%.2fft" % (w), (image.shape[1] - 200, image.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 2.0, (0, 255, 0), 3)
    
    # display results
    #cv2.imshow("mask", blue_mask)
    #cv2.imshow("blue_res", blue_res)



    # HSV COLOURSPACE END


    # DISTANCE BEGIN
def distance_to_camera(knownWidth, focallength, perWidth):
    # calculate and return the distance from the object to the camera
    return (knownWidth * focallength) / perWidth

main()
cap.release()
cv2.destroyAllWindows()
