import requests
import time

def simulate_claude_stream(prompt, num_requests=5, delay=2):
    url = "https://api.anthropic.com/v1/messages"
    headers = {
        "x-api-key": "<MY-SECRET-API-KEY>",
        "anthropic-version": "2023-06-01",
        "content-type": "application/json"
    }
    data = {
        "model": "claude-3-opus-20240229",
        "stream": True,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 512
    }

    for i in range(num_requests):
        print(f"Sending request {i+1}...")
        with requests.post(url, json=data, headers=headers, stream=True) as r:
            for line in r.iter_lines(decode_unicode=True):
                if line:
                    print(line.strip())
        time.sleep(delay)  # simulate realistic usage intervals

# Example usage
simulate_claude_stream("Summarize the history of the internet in 5 points.")

