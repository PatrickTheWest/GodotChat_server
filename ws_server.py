import websockets
import asyncio
import ssl
import pathlib
import json


USER_LIST = set()


async def register_user(websocket):
    print("Registered User")
    USER_LIST.add(websocket)


async def unregister_user(websocket):
    print("Unregistered User")
    USER_LIST.remove(websocket)


async def notify_users(mesg):
    print("sending: ", mesg, " to all users")
    if USER_LIST:
        await asyncio.wait([user.send(mesg) for user in USER_LIST])


async def entry_point(websocket, path):
    # Register a user upon connecting
    await register_user(websocket)
    try:
        greeting = await websocket.recv()
        # Messages sent from Godot end up as bytes objects and have trouble sending back to JavaScript
        if isinstance(greeting, bytes):
            greeting = str(greeting, "utf-8")
        print(greeting)
        await notify_users(greeting)

        while True:
            mesg_recv = await websocket.recv()
            print("recieved: ", mesg_recv)
            mesg_send = process_json(mesg_recv)
            await notify_users(mesg_send)

    finally:
        await unregister_user(websocket)


def process_json(mesg):
    message_contents = json.loads(mesg)
    name = message_contents["name"]
    message = message_contents["message"]
    return f"{name}: {message}"


def run_server(port):
    """ For adding SSL uncomment
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    # Requires certificate chain
    localhost_pem = pathlib.Path(__file__).with_name("fullchain.pem")
    priv_key_pem = pathlib.Path(__file__).with_name("privkey.pem")
    ssl_context.load_cert_chain(localhost_pem, priv_key_pem)

    # Remove the ssl variable to run it insecurely
    # Host field left blank to connect from ALL sources/connections
    start_server = websockets.serve(entry_point, "", port, ssl=ssl_context)
    """

    # Comment this if running SSL
    start_server = websockets.serve(entry_point, "", port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()