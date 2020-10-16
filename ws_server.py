import websockets
import asyncio


async def hello(websocket, path):
    name = await websocket.recv()
    print(f"< {name}")

    greeting = f"Hello {name}!"

    await websocket.send(greeting)

    while True:
        mesg = await websocket.recv()
        print(f"Received: {mesg}")
        await websocket.send(f"{mesg}")

    print(f"< {greeting}")


def run_server(port):
    start_server = websockets.serve(hello, "localhost", port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()