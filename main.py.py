import cv2
from cvzone.HandTrackingModule import HandDetector
from pynput.keyboard import Key, Controller
# import mediapipe as mp

# Initializing camera and hand detector
cap = cv2.VideoCapture(0)
cap.set(3, 720)
cap.set(4, 420)
detector = HandDetector(detectionCon=0.7, maxHands=1)
keyboard = Controller()

while True:
    _, img = cap.read()
    hands, img = detector.findHands(img)
    if hands:
        fingers = detector.fingersUp(hands[0])
        if fingers == [0, 1, 1, 1, 1]:
            if last_key != Key.down:  # Check if the last key pressed was not 'down'
                keyboard.press(Key.down)
                last_key = Key.down
        elif fingers == [0, 1, 0, 0, 0]:
            if last_key != Key.left:
                keyboard.press(Key.left)
                last_key = Key.left
        elif fingers == [0, 1, 1, 0, 0]:
            if last_key != Key.right:
                keyboard.press(Key.right)
                last_key = Key.right
        elif fingers == [1, 1, 1, 1, 1]:
            if last_key != Key.up:
                keyboard.press(Key.up)
                last_key = Key.up
        else:
            # Release all keys if no fingers are in a specific gesture
            keyboard.release(Key.up)
            keyboard.release(Key.down)
            keyboard.release(Key.left)
            keyboard.release(Key.right)
            last_key = None
        
    else:
        # Release all keys if no hands are detected
        keyboard.release(Key.up)
        keyboard.release(Key.down)
        keyboard.release(Key.left)
        keyboard.release(Key.right)
        last_key = None
        
    cv2.imshow("Gesture-Controlled Hill Climb Racing", img)
    if cv2.waitKey(1) == ord("q"):
        break