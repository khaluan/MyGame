import cv2
from turtle import *
import math
import itertools
speed(0)
pencolor('red')
def flatten(list2d):
    return [list(item) for sublist in list2d for item in sublist]

def length(point1, point2):
    return math.dist(point1, point2)

def angle_of_line(line1, line2):
    x1, y1 = line1
    x2, y2 = line2
    return math.degrees(math.atan2((y2-y1), x2-x1))

img = cv2.imread('test.png')
height, width, _ = img.shape
# img = cv2.resize(img, (200, 400))
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
img_blur = cv2.GaussianBlur(img_gray, (3,3), 0) 
sobelx = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=0, ksize=5) # Sobel Edge Detection on the X axis
sobely = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=0, dy=1, ksize=5) # Sobel Edge Detection on the Y axis
sobelxy = cv2.Sobel(src=img_blur, ddepth=cv2.CV_64F, dx=1, dy=1, ksize=5) # Combined X and Y Sobel Edge Detection
edges = cv2.Canny(image=img_blur, threshold1=50, threshold2=150) # Canny Edge Detection

contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# cv2.drawContours(img, contours[:50], -1, (0, 255, 0), -1) #---set the last parameter to -1
# cv2.imshow('Haha', img)
# cv2.waitKey(0)
eps = 0.001

coordinates = []
for contour in contours:
    peri = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, eps * peri, True)
    approx = flatten(approx)
    print(approx)
    coordinates.append(approx)
    # break

coordinates = [[(x, height - y) for (x, y) in poly] for poly in coordinates]    

# cv2.drawContours(img, contours[:50], -1, (0, 255, 0), -1) #---set the last parameter to -1
# for poly in coordinates:
#     print(poly)
#     cv2.polylines(img, poly, False, (255, 0, 0), -1)
# cv2.imshow('Haha', img)
# cv2.waitKey(0)
# exit()
start_x, start_y = 0, 0
for arr in coordinates:
    # print(arr)
    penup()
    x, y = arr[0]
    goto(start_x + x, start_y + y)
    pendown()
    for i in range(1, len(arr)):
        u, v = arr[i]
        angle = angle_of_line(arr[i-1], arr[i])
        if (angle < 0):
            setheading(360 + angle)
        else:
            setheading(angle)
        dist = length(arr[i], arr[i-1])
        forward(dist)

done()

