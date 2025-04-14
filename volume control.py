import cv2
import mediapipe as mp
import numpy as np
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# Initialize MediaPipe Hands
mpHands = mp.solutions.hands
hands = mpHands.Hands()
mpDraw = mp.solutions.drawing_utils

# Initialize camera
cap = cv2.VideoCapture(0)

# Initialize Pycaw for volume control
devices = AudioUtilities.GetSpeakers()
interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
volume = cast(interface, POINTER(IAudioEndpointVolume))

# Get the volume range
volRange = volume.GetVolumeRange()
minVol = volRange[0]
maxVol = volRange[1]

# Map the number of fingers to volume levels
fingerVolumeMap = {
    0: minVol,
    1: minVol + (maxVol - minVol) * 0.2,
    2: minVol + (maxVol - minVol) * 0.4,
    3: minVol + (maxVol - minVol) * 0.6,
    4: minVol + (maxVol - minVol) * 0.8,
    5: maxVol
}

previousFingers = -1

while True:
    success, img = cap.read()
    if not success:
        break

    imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(imgRGB)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mpDraw.draw_landmarks(img, handLms, mpHands.HAND_CONNECTIONS)
            lmList = []
            for id, lm in enumerate(handLms.landmark):
                h, w, c = img.shape
                cx, cy = int(lm.x * w), int(lm.y * h)
                lmList.append((cx, cy))

            if lmList:
                fingers = []
                # Thumb
                if lmList[4][0] > lmList[3][0]:
                    fingers.append(1)
                else:
                    fingers.append(0)
                # Fingers
                for id in range(1, 5):
                    if lmList[4 * id + 4][1] < lmList[4 * id + 2][1]:
                        fingers.append(1)
                    else:
                        fingers.append(0)

                totalFingers = fingers.count(1)
                print(f"Total Fingers: {totalFingers}")

                # Control volume based on the number of fingers
                if totalFingers != previousFingers:
                    vol = fingerVolumeMap[totalFingers]
                    volume.SetMasterVolumeLevel(vol, None)
                    print(f"Volume Set To: {vol}")
                    previousFingers = totalFingers

    cv2.imshow("Image", img)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()