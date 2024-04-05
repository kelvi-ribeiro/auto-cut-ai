import io, json

def save_debug_file(result): 
     print("about to save the debug_file")
     json_data = json.dumps(result, indent=4, ensure_ascii=False)
     with io.open('debug_results/debug.json', 'w', encoding='utf-8') as f:
        f.write(json_data)

def get_debug_file():
     with open('debug_results/debug.json') as f:
         return json.load(f)