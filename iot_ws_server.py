import asyncio
import websockets
import json
from datetime import datetime

connected_devices = set()

async def handle_iot_device(websocket):
    connected_devices.add(websocket)
    print(f"[+] Device connected at {datetime.now()}")

    try:
        async for message in websocket:
            try:
                data = json.loads(message)
                print(f"[Telemetry] {data['device_id']} | Temp: {data['temperature']} | Humidity: {data['humidity']} | Battery: {data['battery']}")
            except json.JSONDecodeError:
                print("[!] Invalid JSON received")

            # Send an ACK to simulate server processing
            ack = {
                "ack": True,
                "received_at": datetime.now().isoformat()
            }
            await websocket.send(json.dumps(ack))

    except websockets.exceptions.ConnectionClosed:
        print(f"[-] Device disconnected at {datetime.now()}")
    finally:
        connected_devices.remove(websocket)

async def main():
    async with websockets.serve(handle_iot_device, "*", 8765):
        print("IoT WebSocket server running at ws://*:8765")
        await asyncio.Future()

asyncio.run(main())
