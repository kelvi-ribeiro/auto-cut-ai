import whisper_timestamped as whisper
import io, json

def get_json_timestamped_result():
    audio = whisper.load_audio("Recording.m4a")

    model = whisper.load_model("tiny", device="cpu")

    return whisper.transcribe(model, audio, language="pt")



result = get_json_timestamped_result()
# Dump JSON data with indentation and ensure_ascii=False for non-ASCII characters
json_data = json.dumps(result, indent=4, ensure_ascii=False)

# Save the JSON data to a file in a human-friendly pretty way
with io.open('data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)