import requests
import json

def main():
    url = 'https://wmch04.deta.dev'
    data = {
        'x': 3,
        'y': 3
    }
    res = requests.post(url, json.dumps(data))
    print(res.json())
    

if __name__ == '__main__':
    main()