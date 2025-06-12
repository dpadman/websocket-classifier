import asyncio
import websockets
import json
import random
import time
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def ai_client():
    uri = "wss://54.176.21.146:8765"
    async with websockets.connect(uri, ssl=ssl_context) as ws:
        for i in range(10):
            data = {
                "prompt": f"Generate response {i}",
                "timestamp": time.time(),
                "type": "ai_inference"
            }
            await ws.send(json.dumps(data))
            response = await ws.recv()
            print("Received:", response)
            await asyncio.sleep(random.uniform(0.5, 2.0))

asyncio.run(ai_client())
