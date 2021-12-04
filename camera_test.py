# from picamera import PiCamera
from time import sleep
import cv2

# camera = PiCamera()
#
# camera.start_preview()
# # camera.start_recording('./video.h264')
# sleep(5)
# # camera.stop_recording()
# camera.stop_preview()


def cam_start(cap, pedestrian_cascade, ball_cascade):

    if cap.isOpened():

        pedestrian_cascade = cv2.CascadeClassifier('./haarcascade_fullbody.xml')
    #
    #     while True:
    #         # reads frames from a video
    #         ret, frames = cap.read()
    #         # convert to gray scale of each frames
    #         #gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
    #         # Detects pedestrians of different sizes in the input image
    #         pedestrians = pedestrian_cascade.detectMultiScale( frames, 1.1,
    #         1)
    #         # To draw a rectangle in each pedestrians
    #         cv2.imshow('Pedestrian detection', frames)
    #         for (x,y,w,h) in pedestrians:
    #             cv2.rectangle(frames,(x,y),(x+w,y+h),(0,255,0),2)
    #             font = cv2.FONT_HERSHEY_DUPLEX
    #             cv2.putText(frames, 'Person', (x + 6, y - 6), font, 0.5, (0,
    #             255, 0), 1)
    #             # Display frames in a window
    #             cv2.imshow('Pedestrian detection', frames)

        ball_cascade = cv2.CascadeClassifier('./ball_cascade.xml')

        while True:
            # reads frames from a video
            ret, frames = cap.read()
            # convert to gray scale of each frames
            #gray = cv2.cvtColor(frames, cv2.COLOR_BGR2GRAY)
            # Detects pedestrians of different sizes in the input image
            pedestrians = pedestrian_cascade.detectMultiScale(frames, 1.1,
            1)
            balls = ball_cascade.detectMultiScale(frames, 1.3,
            3, 8)
            # To draw a rectangle in each pedestrians
            cv2.imshow('Ball detection', frames)
            for (x,y,w,h) in balls:
                cv2.rectangle(frames,(x,y),(x+w,y+h),(0,0,255),2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frames, 'Ball', (x + 6, y - 6), font, 0.5, (0,
                0, 255), 1)
            for (x,y,w,h) in pedestrians:
                cv2.rectangle(frames,(x,y),(x+w,y+h),(0,255,0),2)
                font = cv2.FONT_HERSHEY_DUPLEX
                cv2.putText(frames, 'Person', (x + 6, y - 6), font, 0.5, (0,
                255, 0), 1)

            # Display frames in a window
            cv2.imshow('Ball detection', frames)

    # Wait for Enter key to stop
    #        if cv2.waitKey(33) == 13:
      #          break
   # else:
    #    print('no work')
