import asyncio
import websockets
import aioconsole

async def connect():
    name = input("What's your name? ")
    uri = "ws://137.112.215.152:8000/ws/" + name
    
    async with websockets.connect(uri) as websocket:
        while True:
            messagefromme = await aioconsole.ainput(">")
            await websocket.send(messagefromme)
            messagetome = await websocket.recv()  # Receive messages
            print(messagetome)

            if messagefromme == "EXIT":
                break


asyncio.run(connect())
