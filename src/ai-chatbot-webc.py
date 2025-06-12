import asyncio
import websockets
import json
import time
import random

async def simulate_ai_chat():
    uri = "ws://54.176.21.146:8765"  # Change to your AI WebSocket server
    async with websockets.connect(uri) as ws:
        user_prompts = [
            "What's the capital of France?",
            "Explain how transformers work in AI.",
            "Generate a short poem about the ocean.",
            "Tell me a fun fact about space.",
            "What is the purpose of deep packet inspection?"
        ]

        for i, prompt in enumerate(user_prompts, start=1):
            message = {
                "type": "chat_request",
                "user_id": f"user_{random.randint(1,1000)}",
                "timestamp": time.time(),
                "prompt": prompt
            }
            await ws.send(json.dumps(message))
            print(f"[User] Prompt {i}: {prompt}")

            # Simulate streamed AI response (multiple recv)
            full_response = ""
            for _ in range(random.randint(2, 5)):
                try:
                    chunk = await asyncio.wait_for(ws.recv(), timeout=2)
                    print(f"[AI] {chunk}")
                    full_response += chunk
                    await asyncio.sleep(0.5)
                except asyncio.TimeoutError:
                    print("[AI] No more chunks.")
                    break

            await asyncio.sleep(random.uniform(1, 3))  # simulate think time

asyncio.run(simulate_ai_chat())
