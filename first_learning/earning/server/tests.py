import requests
import json

def main():
    url = "http://localhost:8080/item"
    body = {
        "name": "t-shirt",
        "description": "this is t-shirt",
        "price": 5980,
        "tax": 1.1
    }
    res = requests.post(url, json.dumps(body))
    print(res.json())
    
if __name__ == "__main__":
    main()