# 🤚 YouTube Gesture Controller (Streamlit App)

Control YouTube videos using **hand gestures** via your webcam — all from a clean and simple **Streamlit interface**! This app uses **MediaPipe**, **OpenCV**, and **PyAutoGUI** to recognize gestures and simulate YouTube keyboard shortcuts.

---

## 🎯 Features

- Real-time hand gesture recognition
- Control YouTube playback with:
  - Play / Pause
  - Volume Up / Down
  - Next / Previous video
- Works on **any YouTube tab** open on your computer
- Built with:
  - MediaPipe Hands for gesture detection
  - OpenCV for camera processing
  - PyAutoGUI + keyboard for simulating controls
  - Streamlit for web UI

---

## 🖐️ Gesture Mappings

| Hand Gesture                    | Action          |
|--------------------------------|-----------------|
| All fingers up                 | Play / Pause    |
| All fingers down               | Play / Pause    |
| Index + Middle up              | Volume Up       |
| Ring + Pinky up                | Volume Down     |
| Only Pinky up                  | Next Video      |
| All except Pinky up            | Previous Video  |

> ⚠️ Cooldown of `0.5s` is used to avoid repeated action triggers.

---

## 🚀 How to Run

### 🔧 Requirements

Install the required packages using pip:

```bash
pip install streamlit opencv-python mediapipe numpy keyboard pyautogui
