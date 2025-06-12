import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        print(f"< Received: {message}")
        await websocket.send(f"Echo: {message}")

async def main():
    async with websockets.serve(echo, "*", 8765):
        await asyncio.Future()  # run forever

if __name__ == "__main__":
    asyncio.run(main())
