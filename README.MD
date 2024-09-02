### Introduction

This Python project utilizes artificial intelligence to perform intelligent video cuts based on detected keywords in audio. When a specific word, such as "cut" (configurable as a parameter), is identified, the program automatically segments the video, which can be repeated throughout the entire video. The goal is to simplify the editing of lengthy videos using these tools.

## Dependencies

- ![MoviePy](https://img.shields.io/badge/MoviePy-v1.0.3-blue)
- ![Pedalboard](https://img.shields.io/badge/Pedalboard-v0.9.3-orange)
- ![opencv-python](https://img.shields.io/badge/opencv-python-v4.9.0.80-purple)
- ![Fast_Whisper](https://img.shields.io/badge/Fast_Whisper-v1.0.0-green)
- ![PyQt5](https://img.shields.io/badge/PyQt5-v5.15.11-red)
- ![mediapipe](https://img.shields.io/badge/mediapipe-v0.10.14-yellow)

## Running on Windows

1. Install [FFmpeg](https://www.wikihow.com/Install-FFmpeg-on-Windows)
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run the project:
   ```
   python .\main.py
   ```

## Running on Linux

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
2. Run the project:
   ```
   python main.py
   ```