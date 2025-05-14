import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        # Simulate AI-like streaming response
        for chunk in split_into_chunks(message, chunk_size=20):
            await websocket.send(f"AI: {chunk}")
            await asyncio.sleep(0.4)  # simulate token delay

def split_into_chunks(text, chunk_size):
    return [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]


async def main():
    # start the WebSocket server
    async with websockets.serve(echo, "*", 8765):
        print("AI echo server running on ws://*:8765")
        await asyncio.Future()  # Run forever

# Use asyncio.run() to start the event loop
asyncio.run(main())
