### Introduction

This Python project utilizes artificial intelligence to perform intelligent video cuts based on detected keywords in audio. When a specific word, such as "cut" (configurable as a parameter), is identified, the program automatically segments the video, which can be repeated throughout the entire video. The goal is to simplify the editing of lengthy videos using these tools.

## Dependencies

- ![MoviePy](https://img.shields.io/badge/MoviePy-v1.0.3-blue)
- ![Pedalboard](https://img.shields.io/badge/Pedalboard-v0.9.3-orange)
- ![Fast_Whisper](https://img.shields.io/badge/Fast_Whisper-v1.0.0-green)

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

### Backlog:

- Implement video cutting by gesture.
- Implement automatic cutting after detecting keywords; use default time if not detected.
- Estimate processing time.
- Test from scratch on Windows.
- Implement partial processing to resume from interruption points in videos.