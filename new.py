import cv2
 
cap=cv2.VideoCapture(0)
bg=cv2.flip(cap.read()[1],1)


while True:
    frame=cv2.flip(cap.read()[1],1)
    temp_roi=frame.copy()
    fmask=cv2.absdiff(bg,frame,0)
    fmask=cv2.cvtColor(fmask,cv2.COLOR_BGR2GRAY)
    fmask=cv2.blur(fmask,(10,10))
    fmask=cv2.threshold(fmask,10,255,0)[1]
    fmask=cv2.erode(fmask,cv2.getStructuringElement(cv2.MORPH_ERODE,(2,2)),iterations=2)
    mask1=cv2.morphologyEx(fmask,cv2.MORPH_CLOSE,cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(4,4)))
    mask1=cv2.erode(mask1,cv2.getStructuringElement(cv2.MORPH_ERODE,(2,2)),iterations=2)
    
    con=cv2.findContours(mask1,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[1]
    
    try:
        my_con=max(con,key=cv2.contourArea)
        print (my_con)
    except:
        pass
    
    cv2.imshow('frame',frame)
    cv2.imshow('binary',mask1)
    
    if cv2.waitKey(2)==ord('r'):
        print('Background reset')
        bg=temp_roi;
    elif cv2.waitKey(2)==27:
        break;
cv2.destroyAllWindows();
cap.release();




