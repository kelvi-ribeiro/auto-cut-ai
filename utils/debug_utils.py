import io, json

def save_debug_file(result): 
     print("about to save the debug_file")
     json_data = json.dumps(result, indent=4, ensure_ascii=False)
     with io.open('debug/debug.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

def get_debug_file():
     with open('debug/debug.json') as f:
         return json.load(f)