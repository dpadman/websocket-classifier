import requests

def simulate_non_ai_https():
    urls = [
        "https://www.wikipedia.org",
        "https://httpbin.org/get",
        "https://www.example.com"
    ]
    for url in urls:
        r = requests.get(url)
        print(f"{url} → {r.status_code}")

simulate_non_ai_https()
