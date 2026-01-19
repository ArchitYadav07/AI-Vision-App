import cv2
import numpy as np
from collections import deque

# --- FAIL-SAFE MEDIAPIPE IMPORTS ---
try:
    import mediapipe as mp
    from mediapipe.python.solutions import hands as mp_hands
    from mediapipe.python.solutions import drawing_utils as mp_draw
except ImportError:
    print("MediaPipe is still not fully installed. Try: pip install mediapipe")
    exit()

# Initialize Mediapipe
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7)

# --- DATA STRUCTURES ---
bpoints = [deque(maxlen=1024)]
gpoints = [deque(maxlen=1024)]
rpoints = [deque(maxlen=1024)]
ypoints = [deque(maxlen=1024)]

blue_index = green_index = red_index = yellow_index = 0
colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255), (0, 255, 255)]
colorIndex = 0

# --- CANVAS SETUP ---
paintWindow = np.zeros((471, 636, 3), dtype='uint8') + 255

# Added EXIT button to the list
buttons = [
    ((40,1),(140,65),(0,0,0),"CLEAR"), 
    ((160,1),(255,65),(255,0,0),"BLUE"),
    ((275,1),(370,65),(0,255,0),"GREEN"), 
    ((390,1),(485,65),(0,0,255),"RED"),
    ((505,1),(580,65),(0,255,255),"YELLOW"),
    ((590,1),(635,65),(50,50,50),"EXIT") # New EXIT Button
]

for btn in buttons:
    cv2.rectangle(paintWindow, btn[0], btn[1], btn[2], 2)
    cv2.putText(paintWindow, btn[3], (btn[0][0]+5, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1)

# --- MAIN LOOP ---
cap = cv2.VideoCapture(0)

while True:
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    framergb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # Overlay Buttons on Camera Frame
    for btn in buttons:
        cv2.rectangle(frame, btn[0], btn[1], btn[2], 2)
        cv2.putText(frame, btn[3], (btn[0][0]+5, 33), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,0), 1)

    result = hands.process(framergb)

    if result.multi_hand_landmarks:
        landmarks = []
        for handslms in result.multi_hand_landmarks:
            for lm in handslms.landmark:
                landmarks.append([int(lm.x * 636), int(lm.y * 471)])
            mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)

        center = (landmarks[8][0], landmarks[8][1])
        thumb = (landmarks[4][0], landmarks[4][1])
        
        cv2.circle(frame, center, 8, colors[colorIndex], -1)

        dist = np.hypot(thumb[0]-center[0], thumb[1]-center[1])
        if dist < 35:
            bpoints.append(deque(maxlen=1024)); blue_index += 1
            gpoints.append(deque(maxlen=1024)); green_index += 1
            rpoints.append(deque(maxlen=1024)); red_index += 1
            ypoints.append(deque(maxlen=1024)); yellow_index += 1
        elif center[1] <= 65:
            if 40 <= center[0] <= 140: # Clear
                bpoints, gpoints, rpoints, ypoints = [deque(maxlen=1024)], [deque(maxlen=1024)], [deque(maxlen=1024)], [deque(maxlen=1024)]
                blue_index = green_index = red_index = yellow_index = 0
                paintWindow[67:,:,:] = 255
            elif 160 <= center[0] <= 255: colorIndex = 0
            elif 275 <= center[0] <= 370: colorIndex = 1
            elif 390 <= center[0] <= 485: colorIndex = 2
            elif 505 <= center[0] <= 580: colorIndex = 3
            elif 590 <= center[0] <= 635: # EXIT LOGIC
                print("Exit triggered by Hand Gesture")
                break 
        else:
            if colorIndex == 0: bpoints[blue_index].appendleft(center)
            elif colorIndex == 1: gpoints[green_index].appendleft(center)
            elif colorIndex == 2: rpoints[red_index].appendleft(center)
            elif colorIndex == 3: ypoints[yellow_index].appendleft(center)
    else:
        bpoints.append(deque(maxlen=1024)); blue_index += 1
        gpoints.append(deque(maxlen=1024)); green_index += 1
        rpoints.append(deque(maxlen=1024)); red_index += 1
        ypoints.append(deque(maxlen=1024)); yellow_index += 1

    # DRAWING RENDER
    pts = [bpoints, gpoints, rpoints, ypoints]
    for i in range(len(pts)):
        for j in range(len(pts[i])):
            for k in range(1, len(pts[i][j])):
                if pts[i][j][k-1] is None or pts[i][j][k] is None: continue
                cv2.line(frame, pts[i][j][k-1], pts[i][j][k], colors[i], 2)
                cv2.line(paintWindow, pts[i][j][k-1], pts[i][j][k], colors[i], 2)

    cv2.imshow("Air Canvas", frame)
    cv2.imshow("Paint", paintWindow)
    if cv2.waitKey(1) == ord('q'): break

cap.release()
cv2.destroyAllWindows()