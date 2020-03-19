import cv2
import numpy as np

isHorizontal=True
green_lower=np.array([150,230,0]) #BGR
green_upper=np.array([255,255,140]) #BGR
white_lower=np.array([250,250,250])
white_upper=np.array([255,255,255])

cap = cv2.VideoCapture('http://192.168.0.102:4747/video')
while(True):
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
    ret, image = cap.read()
    image =image[50:-1,50:-1] #to crop the watermark inserted by ip webcam app.
    green_mask=cv2.inRange(image,green_lower,green_upper)
    white_mask=cv2.inRange(image,white_lower,white_upper)
    
    green_output=cv2.bitwise_and(image,image,mask=green_mask)
    gray=cv2.cvtColor(green_output,cv2.COLOR_BGR2GRAY)
    ret,output=cv2.threshold(gray,100,255,0)
    output=cv2.findNonZero(output)
    if output is None:
        cv2.imshow('LiFiReader',image)
        continue
    green_begin=(np.amin(output,0)[0])
    white_output=cv2.bitwise_and(image,image,mask=white_mask)
    gray=cv2.cvtColor(white_output,cv2.COLOR_BGR2GRAY)
    ret,output=cv2.threshold(gray,200,255,0)
    contours, hierarchy = cv2.findContours(output,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(contours)==0:
        cv2.imshow('LiFiReader',image)
        continue
    # for i,c in enumerate(contours):
    #     if cv2.contourArea(c)<50:
    #         contours.pop(i)
    active_led=[]
    voteHorizontal=0
    voteVertical=0
    for x in contours:
        candidate=np.amin(x,0)[0]
        xdiff=abs(candidate[0]-green_begin[0])
        ydiff=abs(candidate[1]-green_begin[1])
        if xdiff<90 or ydiff<90:
            active_led.append(list(candidate))
            if xdiff<90:
                voteHorizontal+=1
            else:
                voteVertical+=1
    if voteHorizontal>voteVertical:
        isHorizontal=True
    else:
        isHorizontal=False
    scale=0
    if(isHorizontal):
        active_led=sorted(active_led,key=lambda l:l[1])
        scale=((active_led[-1][1]-active_led[0][1])/135)*14
    else:
        active_led=sorted(active_led,key=lambda l:l[0])
        scale=((active_led[-1][0]-active_led[0][0])/135)*14
    readInvert=False
    if abs(active_led[0][0]-green_begin[0])>25 and abs(active_led[0][1]-green_begin[1])>25:
        readInvert=True
    bits=[]
    diff=[]
    for i in range(1,len(active_led)):
        if isHorizontal:
            diff.append(active_led[i][1]-active_led[i-1][1])
        else:
            diff.append(active_led[i][0]-active_led[i-1][0])
    for x in diff:
        if x>scale-10:
            bits.append(1)
            for i in range(0,int(round(x/scale))-1):
                bits.append(0)
    value=0
    if readInvert:
        bits.reverse()
        bits=bits[:-1]
    else:
        bits=bits[1:]
    # print(bits)
    if len(bits)!=8:
        cv2.imshow('LiFiReader',image)
        continue
    for i in range(0,len(bits)):
        if i<8:
            value=value|bits[i]<<(7-i)
    cv2.putText(image,"Byte:"+str(value)+" ASCII:"+str(chr(value)),(200,100),cv2.FONT_HERSHEY_SIMPLEX ,1,(0,255,255),thickness=2)
    cv2.imshow('LiFiReader',image)