# Aruco detection program - to be incorporated into Tidy Toys and used to identify the locations to
# drop the toys
# Code tested and working using an Acru Marker created using this web site:
# https://chev.me/arucogen/
# Aruco Dictionary used is 4x4(50, 100, 250, 1000)
# Marker ID - as required, I will probably just used 1, 2 and 3
# Marker size in mm = 100

# Original credit for the code here:
# https://stackoverflow.com/questions/52814747/aruco-opencv-example-all-markers-rejected

import numpy as np
import cv2
import cv2.aruco as aruco

cap = cv2.VideoCapture(0)
while(True):
    ret, frame = cap.read()
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
    parameters = aruco.DetectorParameters_create()
    corners, ids, rejectedImgPoints = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
    print(corners, ids, rejectedImgPoints)
    aruco.drawDetectedMarkers(frame, corners, ids)
    aruco.drawDetectedMarkers(frame, rejectedImgPoints, borderColor=(100, 0, 240))

    cv2.imshow('Display', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
