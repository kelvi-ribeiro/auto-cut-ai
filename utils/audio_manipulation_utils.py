
from pedalboard.io import AudioFile
from pedalboard import *
import noisereduce as nr
import moviepy.editor as mp

def generate_enhenced_audio(video_path):
    clip = mp.VideoFileClip(video_path)
    clip.audio.write_audiofile("extracted_audio.wav")
    sr=44100
    with AudioFile('extracted_audio.wav').resampled_to(sr) as f:
        audio = f.read(f.frames)

        reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.75)

        board = Pedalboard([
            NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
            Compressor(threshold_db=-16, ratio=2.5),
            LowShelfFilter(cutoff_frequency_hz=400, gain_db=10, q=1),
            Gain(gain_db=10)
        ])

        effected = board(reduced_noise, sr)
        audio_enhenced_auth_path = "audio_enhenced.wav"

        with AudioFile(audio_enhenced_auth_path, 'w', sr, effected.shape[0]) as f:
            f.write(effected)
        return audio_enhenced_auth_path