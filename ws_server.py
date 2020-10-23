import websockets
import asyncio
import json


USER_LIST = set()


async def hello(websocket, path):
    name = await websocket.recv()
    print(name)
    await websocket.send(name)

    while True:
        mesg = await websocket.recv()
        print(f"Received: {mesg}")
        await websocket.send(f"{mesg}")


async def register_user(websocket):
    USER_LIST.add(websocket)


async def unregister_user(websocket):
    USER_LIST.remove(websocket)


async def notify_users(mesg):
    if USER_LIST:
        await asyncio.wait([user.send(mesg) for user in USER_LIST])


async def entry_point(websocket, path):
    # Register a user upon connecting
    await register_user(websocket)
    try:
        greeting = await websocket.recv()
        await notify_users(greeting)

        while True:
            mesg = await websocket.recv()
            await notify_users(mesg)

    finally:
        await unregister_user(websocket)


def run_server(port):
    start_server = websockets.serve(entry_point, "localhost", port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()


def parse_message(mesg):
    pass
    # parse message
    # get name
    # get timestamp
    # get message body