from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.io.ffmpeg_tools import ffmpeg_extract_subclip
import speech_recognition as sr
import os

def detect_and_cut(video_path, word_to_detect, output_path):
    clip = VideoFileClip(video_path)

    # Extrai o áudio do vídeo
    audio = clip.audio

    # Salva o áudio em um arquivo temporário
    temp_audio_path = "temp_audio.wav"
    audio.write_audiofile(temp_audio_path)

    # Usa a SpeechRecognition para transcrever o áudio
    recognizer = sr.Recognizer()
    with sr.AudioFile(temp_audio_path) as source:
        audio_data = recognizer.record(source)

    # Realiza a transcrição
    try:
        text = recognizer.recognize_google(audio_data, language='pt-BR')
    except sr.UnknownValueError:
        text = ""

    # Busca a palavra no texto transcrito
    if word_to_detect in text.lower():
            print("Palavra encontrada!")
            ffmpeg_extract_subclip(video_path, 0, 60, targetname=output_path)
    else:
            print("Palavra não encontrada!")
    # Limpa o arquivo temporário
    os.remove(temp_audio_path)

# Exemplo de uso
video_path = "C:\\Users\\kelvi-ribeiro\\Pictures\\Camera Roll\\WIN_20240221_22_27_32_Procom.mp4"
word_to_detect = "gol"
output_path = "C:\\Users\\kelvi-ribeiro\\Pictures\\Camera Roll\\gol.mp4"
detect_and_cut(video_path, word_to_detect, output_path)