import cv2
import numpy as np

# Initial function for the trackbar callback
def hello(x):
    pass

# Initialisation of the camera
cap = cv2.VideoCapture(0)
cv2.namedWindow("bars")

# --- TRACKBARS ---
cv2.createTrackbar("upper_hue", "bars", 110, 180, hello)
cv2.createTrackbar("upper_saturation", "bars", 255, 255, hello)
cv2.createTrackbar("upper_value", "bars", 255, 255, hello)
cv2.createTrackbar("lower_hue", "bars", 68, 180, hello)
cv2.createTrackbar("lower_saturation", "bars", 55, 255, hello)
cv2.createTrackbar("lower_value", "bars", 54, 255, hello)

# --- THE EXIT BUTTON (Trackbar Switch) ---
# 0 = Run, 1 = Exit
cv2.createTrackbar("EXIT (Slide to 1)", "bars", 0, 1, hello)

# Capturing the initial frame for the background
print("Move out of the frame! Capturing background in 2 seconds...")
for i in range(60):
    ret, init_frame = cap.read()
    cv2.waitKey(1)

if not ret:
    print("Failed to grab background frame.")
    cap.release()
    exit()

print("Background captured. You can enter the frame now.")



while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Convert BGR to HSV color space
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Check the Exit Button Status
    exit_status = cv2.getTrackbarPos("EXIT (Slide to 1)", "bars")
    if exit_status == 1:
        print("Exit button triggered. Returning to Dashboard...")
        break

    # Getting the HSV values from trackbars
    u_h = cv2.getTrackbarPos("upper_hue", "bars")
    u_s = cv2.getTrackbarPos("upper_saturation", "bars")
    u_v = cv2.getTrackbarPos("upper_value", "bars")
    l_h = cv2.getTrackbarPos("lower_hue", "bars")
    l_s = cv2.getTrackbarPos("lower_saturation", "bars")
    l_v = cv2.getTrackbarPos("lower_value", "bars")

    # Define the range for the cloak color
    lower_hsv = np.array([l_h, l_s, l_v])
    upper_hsv = np.array([u_h, u_s, u_v])

    # 1. Create a mask to detect the cloak color
    mask = cv2.inRange(hsv_frame, lower_hsv, upper_hsv)
    
    # 2. Refine the mask (remove noise)
    mask = cv2.medianBlur(mask, 3)
    kernel = np.ones((3, 3), dtype='uint8') 
    mask = cv2.dilate(mask, kernel, iterations=2)
    
    # 3. Create an inverted mask for the rest of the scene
    mask_inv = cv2.bitwise_not(mask)

    # 4. The Magic: Combine the frames
    frame_no_cloak = cv2.bitwise_and(frame, frame, mask=mask_inv)
    cloak_area_replaced = cv2.bitwise_and(init_frame, init_frame, mask=mask)

    final_output = cv2.addWeighted(frame_no_cloak, 1, cloak_area_replaced, 1, 0)

    # Add text instructions to the magic screen
    cv2.putText(final_output, "Slide EXIT bar to 1 to quit", (10, 30), 
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    cv2.imshow("Harry's Cloak", final_output)

    # Keep keyboard exit as a backup
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()