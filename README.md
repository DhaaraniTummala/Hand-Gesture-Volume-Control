# Hand Gesture Volume Control

This project uses a webcam, MediaPipe, and Pycaw to control the system volume based on hand gestures. The number of fingers detected determines the volume level.

## Features

- **Hand Tracking**: Uses MediaPipe to detect and track hand landmarks.
- **Volume Control**: Maps the number of fingers shown to specific volume levels.
- **Real-Time Feedback**: Displays the webcam feed with hand landmarks and prints the current volume level in the console.

## Requirements

- Python 3.x
- Required Python libraries:
  - `opencv-python`
  - `mediapipe`
  - `numpy`
  - `pycaw`

## Installation

1. Clone this repository or download the source code.
2. Install the required libraries:
   ```sh
   pip install opencv-python mediapipe numpy pycaw
