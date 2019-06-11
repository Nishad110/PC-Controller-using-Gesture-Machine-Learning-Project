import cv2
import numpy as np
import math
import time
import pyautogui

 
cap=cv2.VideoCapture(0)
bg=cv2.flip(cap.read()[1],1)

pyautogui.FAILSAFE = False
CLICK = CLICK_MESSAGE = MOVEMENT_START = None
p, q, w, h = 300, 100, 300, 300
while True:
    img=cv2.flip(cap.read()[1],1)
    temp_roi=img.copy()
    fmask=cv2.absdiff(bg,img,0)
    fmask=cv2.cvtColor(fmask,cv2.COLOR_BGR2GRAY)
    fmask=cv2.blur(fmask,(10,10))
    fmask=cv2.threshold(fmask,10,255,0)[1]
    fmask=cv2.erode(fmask,cv2.getStructuringElement(cv2.MORPH_ERODE,(2,2)),iterations=2)
    mask1=cv2.morphologyEx(fmask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4)))
    thresh1=cv2.erode(mask1,cv2.getStructuringElement(cv2.MORPH_ERODE,(2,2)),iterations=2)
    #thresh1 = thresh1[q:q+h, p:p+w]
    contours=cv2.findContours(thresh1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    
    try: 
        cnt=max(contours,key=cv2.contourArea)
        hull = cv2.convexHull(cnt, returnPoints=False)
        drawing = np.zeros(img.shape, np.uint8)
        cv2.drawContours(drawing, [cnt], 0, (0, 255, 0), 0)
        defects = cv2.convexityDefects(cnt, hull)
        count_defects = 0
        cv2.drawContours(thresh1, contours, -1, (0, 255, 0), 3)
        used_defect = None

        for i in range(defects.shape[0]):
         s, e, f, d = defects[i, 0]
         start = tuple(cnt[s][0])
         end = tuple(cnt[e][0])
         far = tuple(cnt[f][0])
         a = math.sqrt((end[0] - start[0]) ** 2 + (end[1] - start[1]) ** 2)
         b = math.sqrt((far[0] - start[0]) ** 2 + (far[1] - start[1]) ** 2)
         c = math.sqrt((end[0] - far[0]) ** 2 + (end[1] - far[1]) ** 2)
         angle = math.acos((b ** 2 + c ** 2 - a ** 2) / (2 * b * c)) * 57
         if angle <= 90:
            count_defects += 1
            cv2.circle(img, far, 5, [0, 0, 255], -1)
         cv2.line(img, start, end, [0, 255, 0], 2)

         if count_defects == 1 and angle <= 90:
            used_defect = {"x": far[0], "y": far[1]}

        if used_defect is not None:
         best = used_defect
         if count_defects == 1:
            x = best['x']
            y = best['y']
            display_x = x
            display_y = y

            if MOVEMENT_START is not None:
                M_START = (x, y)
                x = x - MOVEMENT_START[0]
                y = y - MOVEMENT_START[1]
                MOVEMENT_START = M_START
                print("X: " + str(x) + " Y: " + str(y))
                pyautogui.moveRel(x, y)
            else:
                MOVEMENT_START = (x, y)

            cv2.circle(img, (display_x, display_y), 5, [255, 255, 255], 20)
         elif count_defects == 2 and CLICK is None:
            #CLICK = time.time()
            #pyautogui.click()
            CLICK_MESSAGE = "LEFT CLICK"
         elif count_defects == 4 and CLICK is None:
            #CLICK = time.time()
            #pyautogui.rightClick()
            CLICK_MESSAGE = "RIGHT CLICK"
        else:
         MOVEMENT_START = None

        if CLICK is not None:
         cv2.putText(img, CLICK_MESSAGE, (50, 200), cv2.FONT_HERSHEY_SIMPLEX, 3, 3)
         if CLICK < time.time():
             CLICK = None

        cv2.putText(img, "Defects: " + str(count_defects), (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 2, 2)
    except:
        pass   
    
    #cv2.rectangle(img, (p,q), (p+w, q+h), (0,255,0), 2)
    cv2.imshow('frame',img)
    cv2.imshow('binary',thresh1)
    
    if cv2.waitKey(2)==ord('r'):
        print('Background reset')
        bg=temp_roi;
    elif cv2.waitKey(2)==ord('c'):
        break
cv2.destroyAllWindows()
cap.release()
