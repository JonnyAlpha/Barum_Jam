# Tidy_Up_The_Toys PiWars 2021
The object of this challenge is to collect three different coloured
blocks, 50mm x 50mm, red, green and blue and deposit them in a target area.
To gain maximum points, the aim will be to tackle this challenge 
using computer vision with Python OpenCV.
To identify the objects we will be using OpenCV HSV and to calculate the object position, we will be using OpenCV Moments.

# Note on files

README.md - This file
centroid_blue.py - script exploring the use of centroids 
colour_detect_boxed.py - script esploring addinig a bounding box around an identified object
colour_detect_contours.py - script exploring the use of contours to identify the edges of an object
hsv_detect.py - script to calibrate hsv detection
multicolour_detect.py - script used to calibrate hsv detection
object_distance.py - script utilising OpenCV Moments pixel height to calculate distances
object_position.py - script utilising OpenCV Moments object coordinates to calculate relative position
