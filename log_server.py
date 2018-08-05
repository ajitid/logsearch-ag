import asyncio
import json
import websockets
from snippets import get_ip, console

# saac - server as a client
ip = get_ip()

loop = asyncio.get_event_loop()
# loop.set_debug(True)


async def main(uri):
    async with websockets.connect(uri) as websocket:
        await websocket.send(
            json.dumps({
                'type': 'server_info',
                'ip': ip
            })
        )
        # await asyncio.sleep(1000)
        while True:
            text_data = await websocket.recv()
            data = json.loads(text_data)
            # task = loop.create_task(console(cmd))
            # loop.run_until_complete(task)
            result = await console(data['query'])
            result = result.decode("utf-8")
            # print(result)
            # FIXME views later return and asyncio sleep
            # await asyncio.sleep(4)
            await websocket.send(
                json.dumps({
                    'type': 'log_result',
                    'ip': ip,
                    'uid': data['uid'],
                    'result': result
                })
            )

loop.run_until_complete(
    main('ws://localhost:8000/ws/logsearch/log_servers'))
# loop.run_forever()
