import cv2
import matplotlib
import numpy

img = cv2.imread("C:\\Users\\Lenovo\\Desktop\\Web3_Projects\\Kaleidoscope_art_engine_2D\\layers\\Background\\Mountains#100.png", 0)
cv2.imshow("myWindow", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
