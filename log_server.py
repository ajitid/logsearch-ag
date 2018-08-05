import asyncio
import json
import websockets
from snippets import get_ip, console_task

ip = get_ip()

loop = asyncio.get_event_loop()


async def main(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(
            json.dumps({
                'type': 'server_info',
                'ip': ip
            })
        )
        while True:
            text_data = await websocket.recv()
            data = json.loads(text_data)
            asyncio.ensure_future(console_task(
                data['query'], data['uid'], websocket))

loop.run_until_complete(
    main('ws://localhost:8000/ws/logsearch/log_servers'))
