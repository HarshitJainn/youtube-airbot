import streamlit as st
import cv2
import mediapipe as mp
import numpy as np
import time
import keyboard

# Initialize MediaPipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils
tip_ids = [4, 8, 12, 16, 20]

# Initialize session state variables
if 'camera_on' not in st.session_state:
    st.session_state.camera_on = False
if 'action_log' not in st.session_state:
    st.session_state.action_log = []
if 'last_action_time' not in st.session_state:
    st.session_state.last_action_time = 0
if 'last_action' not in st.session_state:
    st.session_state.last_action = None

# Set cooldown time
cooldown = 0.5  # reduced cooldown for better responsiveness

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

def determine_gesture_action(fingers):
    if fingers == [1, 1, 1, 1, 1]:
        return "Play/Pause"
    elif fingers == [0, 0, 0, 0, 0]:
        return "Play/Pause"
    elif fingers == [0, 1, 1, 0, 0]:
        return "Volume Up"
    elif fingers == [0, 0, 0, 1, 1]:
        return "Volume Down"
    elif fingers == [0, 0, 0, 0, 1]:
        return "Next Video"
    elif fingers == [1, 1, 1, 1, 0]:
        return "Previous Video"
    return None

def perform_action(action):
    try:
        if action == "Play/Pause":
            keyboard.press_and_release('space')
        elif action == "Volume Up":
            keyboard.press_and_release('up')
        elif action == "Volume Down":
            keyboard.press_and_release('down')
        elif action == "Next Video":
            keyboard.press_and_release('shift+n')
        elif action == "Previous Video":
            keyboard.press_and_release('shift+p')
    except Exception as e:
        st.error(f"Error performing action: {str(e)}")

def process_webcam():
    cap = cv2.VideoCapture(0)
    camera_placeholder = st.empty()
    
    # Check if camera opened successfully
    if not cap.isOpened():
        st.error("Error: Could not open webcam. Please check your camera connection and permissions.")
        return
    
    try:
        while st.session_state.camera_on:
            # Read frame
            success, img = cap.read()
            if not success:
                st.error("Failed to receive frame from webcam. Check camera connection.")
                break
            
            # Convert to RGB for MediaPipe
            img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            
            # Process with MediaPipe
            results = hands.process(img_rgb)
            
            if results.multi_hand_landmarks:
                for handLms in results.multi_hand_landmarks:
                    # Draw landmarks
                    mp_draw.draw_landmarks(img_rgb, handLms, mp_hands.HAND_CONNECTIONS)
                    
                    # Get finger positions
                    fingers = get_finger_states(handLms)
                    
                    # Display finger state
                    cv2.putText(img_rgb, str(fingers), (10, 70), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
                    
                    # Check for gestures and perform actions with cooldown
                    current_time = time.time()
                    if current_time - st.session_state.last_action_time > cooldown:
                        action = determine_gesture_action(fingers)
                        if action and action != st.session_state.last_action:
                            # Perform the action
                            perform_action(action)
                            
                            # Log the action
                            st.session_state.action_log.append(f"{time.strftime('%H:%M:%S')}: {action}")
                            if len(st.session_state.action_log) > 10:
                                st.session_state.action_log.pop(0)
                            
                            # Display current action on video
                            cv2.putText(img_rgb, f"Action: {action}", (10, 30), 
                                      cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
                            
                            st.session_state.last_action_time = current_time
                            st.session_state.last_action = action
            
            # Display the frame
            camera_placeholder.image(img_rgb, channels="RGB", use_column_width=True)
            
            # Wait for a short time to create real-time effect in Streamlit
            time.sleep(0.01)
            
    finally:
        # Always release the camera when done or on error
        cap.release()

def main():
    # Set page config
    st.set_page_config(page_title="YouTube Gesture Control", layout="wide")
    
    # Title and description
    st.title("YouTube Gesture Control")
    
    # Video URL input
    video_url = st.text_input("Enter YouTube Video URL", "")
    
    # Display instructions
    with st.expander("Gesture Control Instructions", expanded=False):
        st.markdown("""
        ### Available Gestures:
        1. **All fingers up**: Play/Pause
        2. **All fingers down**: Play/Pause
        3. **Index and Middle up**: Volume Up
        4. **Ring and Pinky up**: Volume Down
        5. **Only Pinky up**: Next Video
        6. **All fingers up except Pinky**: Previous Video
        
        *Note: There is a 0.5-second cooldown between actions to prevent accidental triggers.*
        """)
    
    # Create layout with columns
    col1, col2 = st.columns([3, 2])
    
    # Video player column
    with col1:
        st.subheader("Video Player")
        if video_url:
            # Extract video ID from YouTube URL
            if "youtube.com" in video_url or "youtu.be" in video_url:
                if "youtube.com/watch?v=" in video_url:
                    video_id = video_url.split("v=")[1].split("&")[0]
                elif "youtu.be/" in video_url:
                    video_id = video_url.split("youtu.be/")[1].split("?")[0]
                else:
                    st.error("Invalid YouTube URL format")
                    video_id = None
                
                if video_id:
                    # Display embedded YouTube video
                    st.markdown(f"""
                    <iframe width="100%" height="400" src="https://www.youtube.com/embed/{video_id}" 
                    frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; 
                    gyroscope; picture-in-picture" allowfullscreen></iframe>
                    """, unsafe_allow_html=True)
            else:
                st.warning("Please enter a valid YouTube URL")
        else:
            st.info("Enter a YouTube URL to load a video")
    
    # Gesture control column
    with col2:
        st.subheader("Gesture Control Camera")
        
        # Camera control buttons
        col_start, col_stop = st.columns(2)
        with col_start:
            if st.button("START CAMERA"):
                st.session_state.camera_on = True
        with col_stop:
            if st.button("STOP CAMERA"):
                st.session_state.camera_on = False
        
        # Create a placeholder for the camera feed
        if not st.session_state.camera_on:
            # Display blank image when camera is off
            blank_image = np.zeros((300, 400, 3), dtype=np.uint8)
            st.image(blank_image, channels="RGB", use_column_width=True)
        else:
            # Start webcam processing
            process_webcam()
        
        # Action log display
        st.subheader("Action Log")
        log_text = "\n".join(st.session_state.action_log)
        st.text_area("", log_text, height=200, key="action_log_area")

if __name__ == "__main__":
    main()