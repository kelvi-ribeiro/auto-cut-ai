import requests

def get_content(url):    
    try:
        response = requests.get(url)
        response.raise_for_status() 
        return response.content
    except Exception as e:
        print(f"An issue occurred while trying to access the URL '{url}'", e)
        return ""