
import cv2
import numpy as np
import math


cap = cv2.VideoCapture(0)

while(cap.isOpened()):

    _, img = cap.read()
    

    cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    crop_img = img[100:300, 100:300]

    grey = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)


    blurred = cv2.GaussianBlur(grey, (35,35), 0)

    _, thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
    cv2.imshow('Thresholded', thresh1)
    
    
    _, contours, _ = cv2.findContours(thresh1, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    cnt = max(contours, key = lambda x:cv2.contourArea(x))

    hull = cv2.convexHull(cnt,returnPoints = False)

    defects = cv2.convexityDefects(cnt,hull)
    count_defects = 0

    for i in range(defects.shape[0]):
        s,e,f,d = defects[i,0]
        start = tuple(cnt[s][0])
        end = tuple(cnt[e][0])
        far = tuple(cnt[f][0])

        a = math.sqrt((end[0] - start[0])**2 + (end[1] - start[1])**2)
        b = math.sqrt((far[0] - start[0])**2 + (far[1] - start[1])**2)
        c = math.sqrt((end[0] - far[0])**2 + (end[1] - far[1])**2)

        angle = math.acos((b**2 + c**2 - a**2)/(2*b*c)) * 57
       
        if angle <= 90:
            count_defects += 1
            cv2.circle(crop_img,far,1,[255,0,0],3)
        

        cv2.line(crop_img,start,end,[0,255,0],2)
       
    if count_defects == 1:
        cv2.putText(img,"Defects:1", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    elif count_defects == 2:
        cv2.putText(img, "Defects:2", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    elif count_defects == 3:
        cv2.putText(img,"Defects:3", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

    elif count_defects == 4:
        cv2.putText(img,"Defects:4", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)
        exit(0)

    cv2.imshow('Gesture', img)

    k = cv2.waitKey(1)
    if k == 27:
        break
