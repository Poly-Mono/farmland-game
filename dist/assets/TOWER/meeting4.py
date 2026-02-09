import cv2  
import numpy as np

img = cv2.imread("RANDOM.png") 
print(img.shape)
#img = cv2.resize(img, (300, 400))
img = cv2.resize(img, (0,0), fx=0.5, fy=0.5)
img = cv2.blur(img, (10,10))
#img = cv2.boxFilter(img, -1, (10, 10))
#img = cv2.GaussianBlur(img, (9,9), 0)
mask = np.zeros(img.shape[:2], dtype="uint8")
#cv2.circle(mask, (160,200), 165, 255, -1)
#img = cv2.bitwise_and(img, img, mask = mask)
#cv2.imshow("Mask", mask)
#cv2.line(img, (0,0), (width, height), (0,255,0), 6)
#cv2.line(img, (width,0), (0, height), (55,200,255), 3)
#cv2.rectangle(img, (0, 300), (width, height), (255,0,0), 5)
#cv2.rectangle(img, (0, 0), (width, 100), (0,255,0), -1)
#cv2.circle(img, (100, 100), 40, (0,0,255), -1)
#cv2.circle(img, (100, 100), 20, (255,255,255), -1)
#cv2.circle(img, (250, 100), 40, (0,0,255), -1)
#cv2.circle(img, (250, 100), 20, (255,255,255), -1)
#img = cv2.putText(img, "Polonikum", (100, 40), 
#cv2.FONT_HERSHEY_COMPLEX, 1 , (0,0,255), 2)
#img = cv2.putText(img, "OpenCV", (100, height-30), 
#cv2.FONT_HERSHEY_COMPLEX, 1 , (255,255,255), 2)
cv2.imshow("Image", img) 

cv2.waitKey(0)
cv2.destroyAllWindows() 