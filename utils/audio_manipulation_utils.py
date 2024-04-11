
from pedalboard.io import AudioFile
from pedalboard import *
import noisereduce as nr
import moviepy.editor as mp
from utils.constants import AUDIO_PATH
import os

def generate_enhenced_audio(combined_videos, final_video_name):
    extract_audio_path = f"{AUDIO_PATH}{os.sep}{final_video_name}_extract.wav"
    # TODO TALVEZ AQUI TENHA QUE CLONAR O OBJETO PAR NÃO DAR SUBSITUIR O AUDIO ORIGINAL PELO MELHORADO
    combined_videos.audio.write_audiofile(extract_audio_path)
    sr=44100
    with AudioFile(extract_audio_path).resampled_to(sr) as f:
        audio = f.read(f.frames)

        reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.75)

        board = Pedalboard([
            NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
            Compressor(threshold_db=-16, ratio=2.5),
            LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
            Gain(gain_db=10)
        ])

        effected = board(reduced_noise, sr)
        audio_enhenced_path = extract_audio_path.replace("extract", "enhenced")

        with AudioFile(audio_enhenced_path, 'w', sr, effected.shape[0]) as f:
            f.write(effected)
        return audio_enhenced_path
