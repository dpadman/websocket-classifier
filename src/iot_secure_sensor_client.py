import asyncio
import websockets
import json
import random
import time
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
ssl_context.check_hostname = False
ssl_context.verify_mode = ssl.CERT_NONE

async def iot_sensor_client():
    uri = "wss://54.176.21.146:8765"  # Your WebSocket echo or telemetry server

    async with websockets.connect(uri, ssl=ssl_context) as ws:
        for _ in range(20):  # Send 20 telemetry updates
            payload = {
                "device_id": f"sensor_{random.randint(1000,9999)}",
                "timestamp": int(time.time()),
                "temperature": round(random.uniform(20.0, 30.0), 2),
                "humidity": round(random.uniform(30.0, 70.0), 2),
                "battery": round(random.uniform(3.2, 4.2), 2),
                "status": random.choice(["OK", "WARN", "FAIL"])
            }
            message = json.dumps(payload)
            await ws.send(message)
            print(f"[Sent] {message}")

            # Optionally receive a response (e.g., ACK or echo)
            try:
                response = await asyncio.wait_for(ws.recv(), timeout=2)
                print(f"[Received] {response}")
            except asyncio.TimeoutError:
                print("[No response]")

            await asyncio.sleep(random.uniform(1.0, 3.0))  # Delay between sends

asyncio.run(iot_sensor_client())
