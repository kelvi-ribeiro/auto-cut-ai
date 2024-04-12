import re
import unicodedata

def remove_special_chars_and_accents(text):
    text = re.sub(r'[^\w\s]', '', text)
    text = unicodedata.normalize('NFKD', text).encode('ASCII', 'ignore').decode('utf-8')
    return text.lower().replace(" ", "")