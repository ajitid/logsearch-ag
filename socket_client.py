import asyncio
# from subprocess import Popen, PIPE
from asyncio.subprocess import create_subprocess_exec, create_subprocess_shell, PIPE
import websockets

future = asyncio.Future()

loop = asyncio.get_event_loop()
loop.set_debug(True)


# async def sync_console(future, cmd):
#     p = Popen(cmd, shell=True, stdout=PIPE)
#     while p.poll() is None:
#         print("none found")
#         await asyncio.sleep(1)
#     #     # while p is None:
#     #     #     await asyncio.sleep(1)
#     out, err = p.communicate()
#     # return (p.returncode, out, err)
#     print(out)
#     future.set_result('Future is done!')

async def console(cmd):
    p = await create_subprocess_shell(cmd, stdout=PIPE)
    print(await p.stdout.read())


async def hello(uri):
    async with websockets.connect(uri) as websocket:
        while True:
            cmd = await websocket.recv()
            task = loop.create_task(console(cmd))
            loop.run_until_complete(task)
            # subproc(cmd)
            # loop.ensure_future(console(cmd))

            # tasks = [asyncio.ensure_future(do_some_work(2)),
            # asyncio.ensure_future(do_some_work(5))]
            # loop.run_until_complete(asyncio.gather(*tasks))

            # print(console(cmd))
            # # print(await console(cmd))
            # # print()

loop.run_until_complete(
    hello('ws://localhost:8080'))
# loop.run_until_complete(future)
loop.run_forever()

asyncio.subprocess
