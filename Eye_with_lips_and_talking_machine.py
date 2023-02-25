import cv2
import mediapipe as mp
import pyautogui
import speech_recognition as sr
import pyttsx3

listener= sr.Recognizer()
engine= pyttsx3.init()

screen_w, screen_h = pyautogui.size()

cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh()

def talk(text):
    engine.say(text)
    engine.runAndWait()


while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    if landmark_points:
        landmarks = landmark_points[0].landmark
        frame_h, frame_w, _ = frame.shape
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            screen_x = screen_w * landmark.x
            screen_y = screen_h * landmark.y

            #print(x, y)
            #print(left[0].y - left[1].y)
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
        if (left[0].y - left[1].y) < 0.016:
             pyautogui.click()
             print("left click")
        right = [landmarks[386], landmarks[374]]
        for landmark in right:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))

            screen_x = screen_w * landmark.x
            screen_y = screen_h * landmark.y
            pyautogui.moveTo(screen_x, screen_y)
            #print(right[1].y-right[0].y )
            #if (right[1].y-right[0].y) < 0.022:
             #   print("right click")
              #  pyautogui.click(button='right')

        right1 = [landmarks[87], landmarks[20]]
        for landmark in right1:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (255,192, 203))

            screen_x = screen_w * landmark.x
            screen_y = screen_h * landmark.y
            #print(right[0].y - right[1].y)
            if (right1[0].y - right1[1].y) > 0.102:
                pyautogui.press('space')
                talk('Doing scrolling !!')
                print("space")
            # pyautogui.moveTo(screen_x, screen_y)
            # print(right[0].y - right[1].  y)

    cv2.imshow('Eye Controlled mouse', frame)
    cv2.waitKey(1)
