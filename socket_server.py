import asyncio
import websockets


async def echo(websocket, path):
    while True:
        await websocket.send(input())

asyncio.get_event_loop().run_until_complete(
    websockets.serve(echo, 'localhost', 8765))
asyncio.get_event_loop().run_forever()
