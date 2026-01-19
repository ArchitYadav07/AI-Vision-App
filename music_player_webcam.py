import time
import cv2
import os, random
import pygame
import numpy as np
from deepface import DeepFace

# --- 1. SILENCE TENSORFLOW NOISE ---
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
os.environ['TF_ENABLE_ONEDNN_OPTS'] = '0'

# --- 2. SMART PATH SETUP ---
# Locates where THIS script is saved
base_path = os.path.dirname(os.path.abspath(__file__))
xml_name = 'haarcascade_frontalface_alt.xml'

# List of locations to look for the XML brain
possible_paths = [
    os.path.join(base_path, xml_name),                      # Inside AI-Vision-Features
    os.path.join(os.path.dirname(base_path), xml_name),     # Inside CV Projects
    r"C:\Python Programming\CV Projects\Music_player_with_Emotions_recognition\haarcascade_frontalface_alt.xml"
]

xml_path = ""
for path in possible_paths:
    if os.path.exists(path):
        xml_path = path
        break

# --- 3. INITIALIZE COMPONENTS ---
pygame.mixer.init()

if xml_path == "":
    # Visible error window if XML is missing
    error_img = np.zeros((300, 800, 3), dtype='uint8')
    cv2.putText(error_img, "CRITICAL ERROR: XML File Missing!", (50, 100), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)
    cv2.putText(error_img, f"Please copy {xml_name} to {base_path}", (50, 150), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,255,255), 1)
    cv2.imshow("Error", error_img)
    cv2.waitKey(0)
    exit()

classifier = cv2.CascadeClassifier(xml_path)
webcam = cv2.VideoCapture(0)

# Window Setup
window_name = 'AI Emotion Music Player'
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
def nothing(x): pass
cv2.createTrackbar("EXIT (1)", window_name, 0, 1, nothing)

# --- 4. LOGIC VARIABLES ---
current_mood = "Neutral"
last_detected_mood = "Neutral"
start_time = time.time()
music_timer = 5 
size = 4

print("System Starting... Loading DeepFace models (this may take a moment)...")

# --- 5. MAIN LOOP ---
while True:
    (rval, im) = webcam.read()
    if not rval: break
    im = cv2.flip(im, 1, 0)
    
    # Check for manual Exit via Trackbar
    if cv2.getTrackbarPos("EXIT (1)", window_name) == 1:
        pygame.mixer.music.stop()
        break

    mini = cv2.resize(im, (int(im.shape[1] / size), int(im.shape[0] / size)))
    faces = classifier.detectMultiScale(mini)

    detected_this_frame = "Neutral"

    for f in faces:
        (x, y, w, h) = [v * size for v in f]
        sub_face = im[y:y + h, x:x + w]
        FaceFileName = os.path.join(base_path, "test.jpg")
        cv2.imwrite(FaceFileName, sub_face)
        
        try:
            # Analyze face for emotion
            results = DeepFace.analyze(img_path=FaceFileName, 
                                       actions=['emotion'], 
                                       enforce_detection=False,
                                       silent=True)
            detected_this_frame = results[0]['dominant_emotion'].title()
        except:
            detected_this_frame = "Neutral"

        # UI Color mapping
        color = (255, 255, 255) # Neutral
        if detected_this_frame == 'Happy': color = (0, 255, 0)
        elif detected_this_frame == 'Sad': color = (255, 0, 0)
        elif detected_this_frame == 'Angry': color = (0, 0, 255)
        
        cv2.rectangle(im, (x, y), (x + w, y + h), color, 4)
        cv2.putText(im, detected_this_frame, (x, y - 10), cv2.FONT_HERSHEY_TRIPLEX, 0.8, color, 2)

    # --- 6. BACKGROUND MUSIC LOGIC ---
    if detected_this_frame == last_detected_mood:
        elapsed = time.time() - start_time
        if elapsed >= music_timer and detected_this_frame != current_mood:
            current_mood = detected_this_frame
            mood_folder = os.path.join(base_path, "songs", current_mood)
            
            if os.path.exists(mood_folder) and os.listdir(mood_folder):
                randomfile = random.choice(os.listdir(mood_folder))
                full_path = os.path.abspath(os.path.join(mood_folder, randomfile))
                
                try:
                    pygame.mixer.music.load(full_path)
                    pygame.mixer.music.play(-1) # Loop music
                    print(f"Now Playing: {randomfile} ({current_mood} mood)")
                except Exception as e:
                    print(f"Audio Error: {e}")
    else:
        # Mood changed - reset the 5-second timer
        last_detected_mood = detected_this_frame
        start_time = time.time()

    # --- 7. UI OVERLAY ---
    remaining = max(0, music_timer - (time.time() - start_time))
    cv2.rectangle(im, (0,0), (320, 80), (0,0,0), -1)
    cv2.putText(im, f"Mood: {current_mood}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
    if detected_this_frame != current_mood:
        cv2.putText(im, f"Switch in: {int(remaining)}s", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)

    cv2.imshow(window_name, im)
    
    # Backup keyboard exit
    if cv2.waitKey(30) & 0xff == ord('q'): 
        pygame.mixer.music.stop()
        break

webcam.release()
cv2.destroyAllWindows()