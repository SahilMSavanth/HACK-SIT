import cv2
import numpy as np

img=cv2.imread("C:\\Users\\EJ511TS\\OneDrive\\Desktop\\pothole.webp")
'''cvt_rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
hsv=cv2.cvtColor(cvt_rgb,cv2.COLOR_RGB2HSV)
upper_hsv=np.array([10,255,255])
lower_hsv=np.array([8,50,10])
mask=cv2.inRange(hsv,lower_hsv,upper_hsv)


kernel=np.ones((7,7),np.uint8)
mask=cv2.morphologyEx(mask,cv2.MORPH_CLOSE,kernel)
mask=cv2.morphologyEx(mask,cv2.MORPH_OPEN,kernel)

segment_img=cv2.bitwise_and(img,img,mask=mask)
cnts=cv2.findContours(mask.copy(),cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts=cnts[0] if len(cnts) ==2 else cnts[1]
area=0'''

gray= cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
blurred_image = cv2.GaussianBlur(gray, (5, 5), 0)
ret,thresh= cv2.threshold(blurred_image,150,255,cv2.THRESH_BINARY_INV)
cnts, _ = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

for c in cnts:
    area=cv2.contourArea(c)
    bounding__rect=cv2.drawContours(img,[c],-1,(0,255,0),2)
cv2.imshow('',img)
cv2.imshow('thresh',thresh)
cv2.waitKey(0)
