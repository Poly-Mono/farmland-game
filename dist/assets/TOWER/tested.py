import numpy as np
# Tambahkan code di bawah ini
def getContours(img): 
     contours, _ = cv2.findContours(img, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)                                 
     for cnt in contours:  
        area = cv2.contourArea(cnt)
        print(area)                
        cv2.drawContours(imgContour, cnt, -1, (255,0,0), 3)