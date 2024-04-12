
from pedalboard.io import AudioFile
from pedalboard import *
from utils.constants import AUDIO_PATH
import os

def generate_enhenced_audio(combined_videos, final_video_name):
    extract_audio_path = f"{AUDIO_PATH}{os.sep}{final_video_name}_extract.wav"
    sr=44100
    combined_videos.audio.to_audiofile(extract_audio_path, fps=sr)

    with AudioFile(extract_audio_path).resampled_to(sr) as f:
        audio = f.read(f.frames)

    board = Pedalboard([
        NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
        Compressor(threshold_db=-16, ratio=2.5),
        LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
        Gain(gain_db=10)
    ])

    effected = board(audio, sr)
    audio_enhenced_path = extract_audio_path.replace("extract", "enhenced")
    with AudioFile(audio_enhenced_path, 'w', sr, effected.shape[0]) as f:
        f.write(effected)
    return audio_enhenced_path