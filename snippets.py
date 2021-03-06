import socket
import json

############
# getting ip addr
from asyncio.subprocess import create_subprocess_shell, PIPE


def get_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:  # noqa
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

############
# run async console cmd


async def console(cmd):
    p = await create_subprocess_shell(cmd, stdout=PIPE)
    return await p.stdout.read()

#########
# async console cmd as task


async def console_task(cmd, uid, websocket):
    p = await create_subprocess_shell(
        r'ag "ecid\\[\Q' + cmd +
        r'\E\\](.*\n)*?(?=(.*?\necid\\[.*\\]))|(ecid\\[12\\](.*\n)*)" --nonumbers --nobreak --nofilename  ./log2.log',
        stdout=PIPE)
    result = await p.stdout.read()
    result = result.decode("utf-8")
    await websocket.send(
        json.dumps({
            'type': 'log_result',
            'ip': get_ip(),
            'uid': uid,
            'result': result
        })
    )
#########
