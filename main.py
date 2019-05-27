import cv2
import datetime
import imutils
import time
delay = 26
num=1
foto = 0
captura = cv2.VideoCapture("rtsp://192.168.43.1:8080/h264_ulaw.sdp")
firstFrame = None

x1Linha1 = 50
x2Linha1 = x1Linha1
y1Linha1 = 0
y2Linha1 = 200

x1Linha2 = 100
x2Linha2 = x1Linha2
y1Linha2 = 0
y2Linha2 = 200   

def detectar (cnts):
    detectado = False
    for c in cnts:       
#        print(cv2.contourArea(c))
		# if the contour is too small, ignore it
        if cv2.contourArea(c) > 1000:              
            detectado = True 
                   
               
		# compute the bounding box for the contour, draw it on the frame,
		# and update the text
    
    
    return detectado

while(1):
    ret, frame = captura.read()
    frame=cv2.resize(frame,(200,200))
    
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (21, 21), 0)
 
	# if the first frame is None, initialize it
    if firstFrame is None:
        firstFrame = gray
        continue
    

	# compute the absolute difference between the current frame and
	# first frame
    frameDelta = cv2.absdiff(firstFrame, gray)
    
#    cv2.imshow("delta", frameDelta)
    thresh = cv2.threshold(frameDelta, 25, 255, cv2.THRESH_BINARY)[1]
#    cv2.imshow("THS", thresh)
 
	# dilate the thresholded image to fill in holes, then find contours
	# on thresholded image
    thresh = cv2.dilate(thresh, None, iterations=2)
    cv2.imshow("DIL", thresh)
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
  
    detectado = detectar(cnts)    
    
    
    if detectado == True:        
        areas = [cv2.contourArea(cnt) for cnt in cnts]
        maxArea_idx = areas.index(max(areas))
        c = cnts[maxArea_idx]
        (x, y, w, h) = cv2.boundingRect(c)
#        cv2.drawContours(frame, cnt, -1, (0, 255, 0), 3)
        cX = int(x+w/2)
        cY = int(y+h/2)     
        
                
        
         
        if cX > x1Linha1 and cX < x1Linha2:
            cv2.circle(frame,(cX,cY), 3, (0,255,0), -1)
        else:
            cv2.circle(frame,(cX,cY), 3, (0,0,255), -1)
        
    cv2.line(frame,(x1Linha1,y1Linha1),(x2Linha1,y2Linha1),(255,0,0),5)   
    cv2.line(frame,(x1Linha2,y1Linha2),(x2Linha2,y2Linha2),(255,0,0),5)
#        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)  
#        cv2.putText(frame, "Area: {}".format(cv2.contourArea(c)), (x, y),
#    		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
    	# draw the text and timestamp on the frame
#    cv2.putText(frame, "frame: {}".format(num), (10, 20),
#		cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
#    cv2.putText(frame, datetime.datetime.now().strftime("%A %d %B %Y %I:%M:%S%p"),
#		(10, frame.shape[0] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.35, (0, 0, 255), 1)
   
    if num < delay + 1 and detectado == True:
            num += 1
    if detectado == False:
        num = 1
    if num==delay:            
            foto += 1
#            cv2.imshow(str(foto), frame)
            print("foto")
    
        
    	# show the frame and record if the user presses a key
    cv2.imshow("Security Feed", frame)
#    cv2.imshow("Thresh", thresh)
#    cv2.imshow("Frame Delta", frameDelta)
        
 
	# if the `q` key is pressed, break from the lop
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break
    if key == ord("g"):
        firstFrame = None
 
captura.release()
cv2.destroyAllWindows()