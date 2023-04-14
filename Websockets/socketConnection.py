# wss://localhost:5000/v1/api/ws
# smd+265598+{'fields':[31]}

import asyncio
import websockets

async def echo(websocket):
    async for message in websocket:
        await websocket.send(f"Message Received: {message}")

async def main():
    async with websockets.serve(echo, "localhost", 5000):
        await asyncio.Future()  # run forever

asyncio.run(main())