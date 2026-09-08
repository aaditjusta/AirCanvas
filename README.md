# AirCanvas 🎨

AirCanvas is a real-time virtual painting application built using Python, OpenCV, and MediaPipe.

It uses webcam-based hand tracking and gesture recognition to let users draw, select colors, and erase using hand gestures.

## Features

☝️ Index finger to draw
✌️ Two fingers to select colors
✋ Palm gesture to erase
🎨 Red, Green, and Blue color selection
📷 Real-time webcam hand tracking

## Technologies Used

Python
OpenCV
MediaPipe
NumPy

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt
```

Run the application:

```bash
python CV.py
```

## Controls

☝️ Index finger → Draw
✌️ Two fingers → Select color
✋ Open palm → Erase
ESC → Exit

## Project Overview

The project uses MediaPipe Hand Landmarks to track the user's hand through a webcam. Specific finger positions are analyzed to recognize gestures, which are then mapped to drawing, color selection, and erasing actions in OpenCV.
