import asyncio
import websockets
import json
import time
import random
import ssl


ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def simulate_llm_client():
    uri = "wss://54.176.21.146:8765"
    prompts = [
        "How do you explain dasavatar to a child?",
        "Explain ed25519 and its fast signing capabilities.",
        "How does MS Dhoni's helicopter shot work?",
        "What are the real names of SWAT Kats?",
        "Generate a Python function to check if a number is a power of 2."
    ]

    async with websockets.connect(uri, ssl=ssl_context) as ws:
        for prompt in prompts:
            message = {
                "prompt": prompt,
                "timestamp": time.time(),
                "session_id": f"user_{random.randint(1000,9999)}"
            }
            await ws.send(json.dumps(message))
            print(f"[Sent prompt] {prompt}")

            full_reply = []
            try:
                while True:
                    token = await asyncio.wait_for(ws.recv(), timeout=1.5)
                    print(f"[Token] {token}")
                    if token == "[end]":
                        break
                    full_reply.append(token)
            except asyncio.TimeoutError:
                print("[Done receiving tokens]")

            await asyncio.sleep(2)

asyncio.run(simulate_llm_client())
