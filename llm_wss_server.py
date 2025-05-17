import asyncio
import websockets
import json
import ssl
import random

def simulate_llm_response(prompt):
    base_response = f"[MyChatGPT] Here's what I found about '{prompt}':"
    tokens = base_response.split() + ["..."] + ["[end]"]
    return tokens

async def handler(websocket):
    async for message in websocket:
        try:
            data = json.loads(message)
            prompt = data.get("prompt", "Hello?")
        except:
            prompt = message

        tokens = simulate_llm_response(prompt)
        for token in tokens:
            await websocket.send(token)
            await asyncio.sleep(random.uniform(0.05, 0.2))  # token delay

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
ssl_context.load_cert_chain(certfile="cert.pem", keyfile="key.pem")

async def main():
    async with websockets.serve(handler, "*", 8765, ssl=ssl_context):
        print("LLM WebSocket server running at wss://*:8765")
        await asyncio.Future()

asyncio.run(main())
