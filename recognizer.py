# from typing import ClassVar
import cv2
import servo
import time

webcam = cv2.VideoCapture(0)
IMG_WIDTH = 320*2
IMG_HEIGHT = 240*2				# Get ready to start getting images from the webcam
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)		# I have found this to be about the highest-
webcam.set(cv2.CAP_PROP_FRAME_HEIGHT, IMG_HEIGHT)

frontalface = cv2.CascadeClassifier("haarcascade_frontalface_alt2.xml")		# frontal face pattern detection
profileface = cv2.CascadeClassifier("haarcascade_profileface.xml")		# side face pattern detection

face = [0,0,0,0]	# This will hold the array that OpenCV returns when it finds a face: (makes a rectangle)
Cface = [0,0]		# Center of the face: a point calculated from the above variable
lastface = 0		# int 1-3 used to speed up detection. The script is looking for a right profile face,-

(pan_servo, tilt_servo) = servo.initialize_servos()
pan_config = servo.pan_config
tilt_config = servo.tilt_config

def show_cam():
    webcam = cv2.VideoCapture(0)

    while True:
        _, img = webcam.read()
        cv2.imshow('smile!', img)
        cv2.waitKey(1) 
    
def detect_faces(frame, frontal=True ):
    if frontal:
        return frontalface.detectMultiScale(frame,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
    
    return profileface.detectMultiScale(frame,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))

def draw_rect_around_faces(frame, faces):
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

def recognize():
    global pan_servo, pan_config, tilt_servo, tilt_config

    while True:
        _, frame = webcam.read()

        faces = detect_faces(frame)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        if len(faces) != 0:
            (x,y,w,h) = faces[0]
            face_center_point = [(w/2+x),(h/2+y)]
            print('face x:{}, y:{}'.format(face_center_point[0], face_center_point[1]))
            width_diff = IMG_WIDTH/2 - face_center_point[0]
            if abs(width_diff) > 20:
                #TODO think of a better way
                angle_to_move = width_diff * 0.05
                new_angle = pan_config.angle + angle_to_move
                print('old width angle: ', pan_config.angle)
                print('width angle: ', new_angle)
                servo.move(pan_servo, pan_config, new_angle)

            height_diff = IMG_HEIGHT/2 - face_center_point[1]
            if abs(height_diff) > 20:
                #TODO think of a better way
                angle_to_move = height_diff * 0.05
                new_angle = tilt_config.angle + angle_to_move
                print('old height angle: ', tilt_config.angle)
                print('height angle: ', new_angle)
                servo.move(tilt_servo, tilt_config, new_angle)
        # else:
            # pan_middle = pan_config.min_duty + pan_config.duty_range/2
            # tilt_middle = tilt_config.min_duty + tilt_config.duty_range/2
            # servo.move(pan_servo, pan_config, servo.duty_to_angle(pan_middle, pan_config.duty_range, pan_config.min_duty, 180))
            # servo.move(tilt_servo, tilt_config, servo.duty_to_angle(tilt_middle, tilt_config.duty_range, tilt_config.min_duty, 180))
            # servo.move(pan_servo, pan_config, pan_config.angle)

        #time.sleep(0.1)
        #cv2.imshow('smile!', frame)
        cv2.waitKey(1)

def recognize2():
    global frontalface, profileface, face, Cface, lastface

    while True:

        faceFound = False	# This variable is set to true if, on THIS loop a face has already been found
                    # We search for a face three diffrent ways, and if we have found one already-
                    # there is no reason to keep looking.
        
        if not faceFound:
            if lastface == 0 or lastface == 1:
                frame = webcam.read()[1]	# there seems to be an issue in OpenCV or V4L or my webcam-
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                # aframe = webcam.read()[1]	# 	driver, I'm not sure which, but if you wait too long,
                # aframe = webcam.read()[1]	#	the webcam consistantly gets exactly five frames behind-
                # aframe = webcam.read()[1]	#	realtime. So we just grab a frame five times to ensure-
                # aframe = webcam.read()[1]	#	we have the most up-to-date image.
                # fface = frontalface.detectMultiScale(aframe,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
                frontal_faces = detect_faces(frame, frontal=True)
                if frontal_faces != ():			# if we found a frontal face...
                    draw_rect_around_faces(frame, frontal_faces)
                    cv2.imshow('frame', frame)
                    lastface = 1		# set lastface 1 (so next loop we will only look for a frontface)
                    for f in frontal_faces:		# f in fface is an array with a rectangle representing a face
                        faceFound = True
                        face = f

        if not faceFound:				# if we didnt find a face yet...
            if lastface == 0 or lastface == 2:	# only attempt it if we didn't find a face last loop or if-
                frame = webcam.read()[1]	# 	THIS method was the one who found it last loop
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                # cv2.imshow('frame', aframe)
                
                # aframe = webcam.read()[1]
                # aframe = webcam.read()[1]	# again we grab some frames, things may have gotten stale-
                # aframe = webcam.read()[1]	# since the frontalface search above
                # aframe = webcam.read()[1]
                # pfacer = profileface.detectMultiScale(aframe,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))
                profile_faces = detect_faces(frame, frontal=False)
                if profile_faces != ():		# if we found a profile face...
                    draw_rect_around_faces(frame, profile_faces)
                    cv2.imshow('frame', frame)
                    lastface = 2
                    for f in profile_faces:
                        faceFound = True
                        face = f

        if not faceFound:				# a final attempt
            if lastface == 0 or lastface == 3:	# this is another profile face search, because OpenCV can only-
                frame = webcam.read()[1]	#	detect right profile faces, if the cam is looking at-
                cv2.imshow('frame', frame)
                cv2.waitKey(1)
                # aframe = webcam.read()[1]	#	someone from the left, it won't see them. So we just...
                # aframe = webcam.read()[1]
                # aframe = webcam.read()[1]
                # aframe = webcam.read()[1]
                cv2.flip(frame,1,frame)	#	flip the image
                # pfacel = profileface.detectMultiScale(frame,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(80,80))
                profile_faces = detect_faces(frame, frontal=False)
                
                if profile_faces != ():
                    draw_rect_around_faces(frame, profile_faces)
                    cv2.imshow('frame', frame)
                    lastface = 3
                    for f in profile_faces:
                        faceFound = True
                        face = f

        if not faceFound:		# if no face was found...-
            lastface = 0		# 	the next loop needs to know
            face = [0,0,0,0]	# so that it doesn't think the face is still where it was last loop


        x,y,w,h = face
        Cface = [(w/2+x),(h/2+y)]	# we are given an x,y corner point and a width and height, we need the center
        print(str(Cface[0]) + "," + str(Cface[1]))

        #draw here maybe

        # if Cface[0] != 0:		# if the Center of the face is not zero (meaning no face was found)

        #     if Cface[0] > 180:	# The camera is moved diffrent distances and speeds depending on how far away-
        #         CamLeft(5,1)	#	from the center of that axis it detects a face
        #     if Cface[0] > 190:	#
        #         CamLeft(7,2)	#
        #     if Cface[0] > 200:	#
        #         CamLeft(9,3)	#

        #     if Cface[0] < 140:	# and diffrent dirrections depending on what side of center if finds a face.
        #         CamRight(5,1)
        #     if Cface[0] < 130:
        #         CamRight(7,2)
        #     if Cface[0] < 120:
        #         CamRight(9,3)

        #     if Cface[1] > 140:	# and moves diffrent servos depending on what axis we are talking about.
        #         CamDown(5,1)
        #     if Cface[1] > 150:
        #         CamDown(7,2)
        #     if Cface[1] > 160:
        #         CamDown(9,3)

        #     if Cface[1] < 100:
        #         CamUp(5,1)
        #     if Cface[1] < 90:
        #         CamUp(7,2)
        #     if Cface[1] < 80:
        #         CamUp(9,3)
    
    cv2.destroyAllWindows()
            
if __name__ == '__main__':
    recognize()
