import cv2
import mediapipe as mp
import keyboard
import time

# Initialize MediaPipe and variables
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]
last_action_time = 0
cooldown = 2  # seconds

def get_finger_states(hand_landmarks):
    fingers = []

    if hand_landmarks.landmark[tip_ids[0]].x < hand_landmarks.landmark[tip_ids[0] - 1].x:
        fingers.append(1)
    else:
        fingers.append(0)
    for i in range(1, 5):
        if hand_landmarks.landmark[tip_ids[i]].y < hand_landmarks.landmark[tip_ids[i] - 2].y:
            fingers.append(1)
        else:
            fingers.append(0)
    
    return fingers

def perform_gesture_action(fingers):
    global last_action_time
    current_time = time.time()

    if current_time - last_action_time < cooldown:
        return

    if fingers == [1, 1, 1, 1, 1]:
        keyboard.press_and_release('k')
        print("Play")
    elif fingers == [0, 0, 0, 0, 0]:
        keyboard.press_and_release('k')
        print("Pause")
    elif fingers == [0, 1, 1, 0, 0]:
        keyboard.press_and_release('up')
        print("Volume Up")
    elif fingers == [0, 0, 0, 1, 1]:
        keyboard.press_and_release('down')
        print("Volume Down")
    elif fingers == [0, 0, 0, 0, 1]:
        keyboard.press('shift')
        keyboard.press_and_release('n')
        keyboard.release('shift')
        print("Next Video")
    elif fingers == [1, 1, 1, 1, 0]:
        keyboard.press('shift')
        keyboard.press_and_release('p')
        keyboard.release('shift')
        print("Previous Video")

    last_action_time = current_time

print("YouTube Gesture Control Started!")
print("Press 'ESC' to exit")
print("Available Gestures:")
print("1. All fingers up: Play/Pause")
print("2. All fingers down: Play/Pause")
print("3. Index and Middle up: Volume Up")
print("4. Ring and Pinky up: Volume Down")
print("5. Only Pinky up: Next Video")
print("6. All fingers up except Pinky: Previous Video")

# Main loop
cap = cv2.VideoCapture(0)

while True:
    success, img = cap.read()
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = hands.process(img_rgb)

    if results.multi_hand_landmarks:
        for handLms in results.multi_hand_landmarks:
            mp_draw.draw_landmarks(img, handLms, mp_hands.HAND_CONNECTIONS)
            fingers = get_finger_states(handLms)
            perform_gesture_action(fingers)
            cv2.putText(img, str(fingers), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,0,0), 2)

    cv2.imshow("YouTube Gesture Controller", img)
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
