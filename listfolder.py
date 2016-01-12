import requests
import json

def main():
    url = "https://api.dropboxapi.com/2/files/list_folder"

    headers = {
    "Authorization": 
        "Bearer BxPEAxwxIbQAAAAAAAAAMGbPJDrPhVeV-vWjEAGf76r1nLV-BOcehGTibHj2xFmb",
    "Content-Type":  "application/json"
    }

    data = {
    "path":               "",
    "recursive":          True,
    "include_media_info": True,
    "include_deleted":    True
    }

    r = requests.post(url, headers=headers, data=json.dumps(data));

    json_data = json.loads(r.text);
    print([ data['name'] for data in json_data['entries']]);

    return r;
