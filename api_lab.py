# api_lab.py
# Initial API lab scaffold

import requests

if __name__ == "__main__":
    print("api_lab.py created successfully")
    try:
        r = requests.get('https://httpbin.org/get')
        print('API status:', r.status_code)
    except Exception as e:
        print('Request failed:', e)
