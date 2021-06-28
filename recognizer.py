from typing import ClassVar
import cv2
import servo

webcam = cv2.VideoCapture(0)				# Get ready to start getting images from the webcam
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_WIDTH, 320)		# I have found this to be about the highest-
webcam.set(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT, 240)

frontalface = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")		# frontal face pattern detection
profileface = cv2.CascadeClassifier("haarcascade_profileface.xml")		# side face pattern detection

face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]		# Center of the face: a point calculated from the above variable
lastface = 0		# int 1-3 used to speed up detection. The script is looking for a right profile face,-

def detect_face():
    while True:

        faceFound = False	# This variable is set to true if, on THIS loop a face has already been found
                    # We search for a face three diffrent ways, and if we have found one already-
                    # there is no reason to keep looking.
        
        if not faceFound:
            if lastface == 0 or lastface == 1:
                aframe = webcam.read()[1]	# there seems to be an issue in OpenCV or V4L or my webcam-
                aframe = webcam.read()[1]	# 	driver, I'm not sure which, but if you wait too long,
                aframe = webcam.read()[1]	#	the webcam consistantly gets exactly five frames behind-
                aframe = webcam.read()[1]	#	realtime. So we just grab a frame five times to ensure-
                aframe = webcam.read()[1]	#	we have the most up-to-date image.
                fface = frontalface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(60,60))
                if fface != ():			# if we found a frontal face...
                    lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
                    for f in fface:		# f in fface is an array with a rectangle representing a face
                        faceFound = True
                        face = f

        if not faceFound:				# if we didnt find a face yet...
            if lastface == 0 or lastface == 2:	# only attempt it if we didn't find a face last loop or if-
                aframe = webcam.read()[1]	# 	THIS method was the one who found it last loop
                aframe = webcam.read()[1]
                aframe = webcam.read()[1]	# again we grab some frames, things may have gotten stale-
                aframe = webcam.read()[1]	# since the frontalface search above
                aframe = webcam.read()[1]
                pfacer = profileface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(80,80))
                if pfacer != ():		# if we found a profile face...
                    lastface = 2
                    for f in pfacer:
                        faceFound = True
                        face = f

        if not faceFound:				# a final attempt
            if lastface == 0 or lastface == 3:	# this is another profile face search, because OpenCV can only-
                aframe = webcam.read()[1]	#	detect right profile faces, if the cam is looking at-
                aframe = webcam.read()[1]	#	someone from the left, it won't see them. So we just...
                aframe = webcam.read()[1]
                aframe = webcam.read()[1]
                aframe = webcam.read()[1]
                cv2.flip(aframe,1,aframe)	#	flip the image
                pfacel = profileface.detectMultiScale(aframe,1.3,4,(cv2.cv.CV_HAAR_DO_CANNY_PRUNING + cv2.cv.CV_HAAR_FIND_BIGGEST_OBJECT + cv2.cv.CV_HAAR_DO_ROUGH_SEARCH),(80,80))
                if pfacel != ():
                    lastface = 3
                    for f in pfacel:
                        faceFound = True
                        face = f

        if not faceFound:		# if no face was found...-
            lastface = 0		# 	the next loop needs to know
            face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop


        x,y,w,h = face
        Cface = [(w/2+x),(h/2+y)]	# we are given an x,y corner point and a width and height, we need the center
        print(str(Cface[0]) + "," + str(Cface[1]))

        if Cface[0] != 0:		# if the Center of the face is not zero (meaning no face was found)

            if Cface[0] > 180:	# The camera is moved diffrent distances and speeds depending on how far away-
                CamLeft(5,1)	#	from the center of that axis it detects a face
            if Cface[0] > 190:	#
                CamLeft(7,2)	#
            if Cface[0] > 200:	#
                CamLeft(9,3)	#

            if Cface[0] < 140:	# and diffrent dirrections depending on what side of center if finds a face.
                CamRight(5,1)
            if Cface[0] < 130:
                CamRight(7,2)
            if Cface[0] < 120:
                CamRight(9,3)

            if Cface[1] > 140:	# and moves diffrent servos depending on what axis we are talking about.
                CamDown(5,1)
            if Cface[1] > 150:
                CamDown(7,2)
            if Cface[1] > 160:
                CamDown(9,3)

            if Cface[1] < 100:
                CamUp(5,1)
            if Cface[1] < 90:
                CamUp(7,2)
            if Cface[1] < 80:
                CamUp(9,3)
            
if __name__ == '__main__':
    detect_face()