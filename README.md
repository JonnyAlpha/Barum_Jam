# 'Tidy up the Toys' PiWars challenge (2021)

The object of this challenge is to collect three different coloured
blocks, 50mm x 50mm, red, green and blue and deposit them in a target area.

To gain maximum points, the aim will be to tackle this challenge
using computer vision with OpenCV's Python module

To identify the objects we will be using OpenCV HSV and to calculate
the object position, we will be using OpenCV Moments.

## Notes on files

- `README.md`

    This file.

- `centroid_blue.py`

     script exploring the use of centroids.

- `colour_detect_boxed.py`

    A script exploring adding a bounding box around an identified object

- `colour_detect_contours.py`

    A script exploring the use of contours to identify the edges of an object.

- `hsv_detect.py`

    A script to calibrate HSV detection.

- `multicolour_detect.py`

    A script used to calibrate HSV detection.

- `object_distance.py`

    A script utilising OpenCV Moments pixel height to calculate distances

- `object_position.py`

    A script utilising OpenCV Moments object coordinates to calculate relative position
    
- `tidy_toys.py`
    
    The actual script for the Tidy Up The Toys challenge.
