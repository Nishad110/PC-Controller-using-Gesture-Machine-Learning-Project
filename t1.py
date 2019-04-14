import cv2
import numpy as np
import math

cap = cv2.VideoCapture(1)

while(cap.isOpened()):
    _, crop_img = cap.read()
    lower = np.array([0, 48, 80], dtype = "uint8")
    upper = np.array([20, 255, 255], dtype = "uint8")
    lower_YCbCr_values = np.array((0, 138, 67), dtype = "uint8")
    upper_YCbCr_values = np.array((255, 173, 133), dtype = "uint8")
    #cv2.rectangle(img,(300,300),(100,100),(0,255,0),0)
    #crop_img = img[100:300, 100:300]
    img_hsv = cv2.cvtColor(crop_img,cv2.COLOR_BGR2HSV)
    YCbCr_image = cv2.cvtColor(crop_img, cv2.COLOR_BGR2YCR_CB)
    mask_YCbCr = cv2.inRange(YCbCr_image, lower_YCbCr_values, upper_YCbCr_values)
    skinMask = cv2.inRange(img_hsv, lower, upper)
    binary_mask_image = cv2.add(skinMask,mask_YCbCr)
    image_foreground = cv2.erode(binary_mask_image,None,iterations = 3)
    dilated_binary_image = cv2.dilate(binary_mask_image,None,iterations = 3)
    blurred = cv2.GaussianBlur(dilated_binary_image, (35,35), 0)  
    _,thresh1 = cv2.threshold(blurred, 127, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    cv2.imshow('Binary', thresh1)
    _, contours, _ = cv2.findContours(thresh1.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
    
    if contours!=[]:
      cnt = max(contours, key = lambda x: cv2.contourArea(x))
    
      x,y,w,h = cv2.boundingRect(cnt)
      cv2.rectangle(crop_img,(x,y),(x+w,y+h),(0,0,255),0)



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
          cv2.putText(crop_img,"Defects:1", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

      elif count_defects == 2:
          cv2.putText(crop_img, "Defects:2", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

      elif count_defects == 3:
          cv2.putText(crop_img,"Defects:3", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

      elif count_defects == 4:
          cv2.putText(crop_img,"Defects:4", (5,50), cv2.FONT_HERSHEY_SIMPLEX, 1, 2)

      cv2.imshow('image', crop_img)
    else:
      cv2.imshow('image', crop_img)
    k = cv2.waitKey(10)
    if k == 27:
        break
