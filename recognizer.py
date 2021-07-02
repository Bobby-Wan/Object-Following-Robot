# from typing import ClassVar
import cv2
import servo
import time

webcam = cv2.VideoCapture(0)
IMG_WIDTH = 320*2
IMG_HEIGHT = 240*2				
webcam.set(cv2.CAP_PROP_FRAME_WIDTH, IMG_WIDTH)		
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
    
def detect_faces(frame):
    faces = frontalface.detectMultiScale(frame,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
    faces  += profileface.detectMultiScale(frame,1.3,4,(cv2.CASCADE_DO_CANNY_PRUNING + cv2.CASCADE_FIND_BIGGEST_OBJECT + cv2.CASCADE_DO_ROUGH_SEARCH),(60,60))
    
    return faces

def draw_rect_around_faces(frame, faces):
    for (x,y,w,h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

def recognize():
    global pan_servo, pan_config, tilt_servo, tilt_config

    fourcc = cv2.VideoWriter_fourcc(*'MJPG')
    video_writer = cv2.VideoWriter('output.avi', fourcc, 20.0, (640, 480))

    while True:
        _, frame = webcam.read()

        faces = detect_faces(frame)
        
        for (x,y,w,h) in faces:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 2)

        video_writer.write(frame)

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

        # cv2.imshow('smile!', frame)
        cv2.waitKey(1)
            
if __name__ == '__main__':
    recognize()
