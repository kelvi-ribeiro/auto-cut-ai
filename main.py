import io, json
import whisper_integration as whis;

result = whis.get_json_timestamped_result("gostaria")
# Dump JSON data with indentation and ensure_ascii=False for non-ASCII characters
json_data = json.dumps(result, indent=4, ensure_ascii=False)

# Save the JSON data to a file in a human-friendly pretty way
with io.open('data.json', 'w', encoding='utf-8') as f:
    f.write(json_data)