# 🎥 YouTube Gesture Controller - Chrome Extension

Control YouTube videos using **hand gestures** via your **webcam**, powered by MediaPipe Hands in JavaScript.

This Chrome Extension overlays a webcam feed on YouTube and maps specific hand gestures to common playback actions like **Play/Pause**, **Volume Up/Down**, **Next**, and **Previous Video**.

---

## 🚀 Features

- 🎯 Real-time gesture detection using MediaPipe Hands JS
- ✋ Recognizes various hand poses with a single hand
- 🔊 Simulates YouTube player controls (play, pause, volume, navigation)
- 🖥️ Works directly on any YouTube tab
- 🌐 100% client-side, no server or backend required

---

## 🖐️ Gesture-to-Action Mapping

| Gesture                        | Action         |
|-------------------------------|----------------|
| All fingers up                | Play / Pause   |
| All fingers down              | Play / Pause   |
| Index + Middle finger up      | Volume Up      |
| Ring + Pinky finger up        | Volume Down    |
| Only Pinky up                 | Next Video     |
| All fingers except Pinky up   | Previous Video |

> ℹ️ A 0.5-second cooldown is used to avoid repeated triggers.

---

## 📁 Project Structure

```bash
youtube-gesture-extension/
├── manifest.json           # Chrome extension config
├── content.js              # Injects webcam and gesture logic into YouTube
├── hand-gesture.js         # Core gesture recognition logic
├── style.css               # Optional styling
├── popup.html              # Optional UI for extension popup
├── popup.js                # Optional popup script
└── README.md
