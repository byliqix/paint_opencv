# Magic Paint - Hand Gesture Drawing

A real-time drawing app using hand gestures detected via MediaPipe and OpenCV.

## Requirements

- Python 3.8+
- Webcam

## Installation

```bash
pip install -r requirements.txt
```

Download the gesture recognition model:

```bash
mkdir -p ~/.mediapipe/models
wget -O ~/.mediapipe/models/gesture_recognizer.task \
  https://storage.googleapis.com/mediapipe-models/gesture_recognizer/gesture_recognizer/float16/latest/gesture_recognizer.task
```

## Usage

```bash
python main.py
```

## Gestures

| Gesture       | Action                        |
|---------------|-------------------------------|
| Pointing_Up   | Draw with sparkle trail       |
| Open_Palm     | Draw (wider, more sparkles)   |
| ILoveYou      | Draw (wider, more sparkles)   |
| Closed_Fist   | Clear canvas                  |
| Gesture change| Burst of sparkles + rune      |

Press `C` to clear the canvas, `ESC` to exit.
