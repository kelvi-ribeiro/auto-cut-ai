### Introduction

AutoCut A.I is a Python program that automates the process of video editing by identifying and cutting sections of videos based on various recognition techniques, including voice, gesture, and blink screen recognition. It combines multiple video files, processes them according to the selected recognition method, and generates a final edited video with precise cuts. The system also includes notifications and email updates on the processing status, ensuring efficient and informed video production.

![short-version.gif](https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExcDdjc2xoaDVweG52eW9wMnA1eWdvODZ3aGRhbGlmNTI0cnFsYmU4OSZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/LcnQpIZzmh1F7SZ8De/giphy.gif)

## Dependencies

- ![MoviePy](https://img.shields.io/badge/MoviePy-v1.0.3-blue)
- ![Pedalboard](https://img.shields.io/badge/Pedalboard-v0.9.3-orange)
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
### Creating a exe file

1. Install pyinstaller
```
pip install pyinstaller
```
2. Run the command to create the exe file
```
python -m PyInstaller --onefile --noconsole --icon=icon_path .\main.py
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