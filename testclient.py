import asyncio
import websockets
import aioconsole  # Asynchronous console input
import keyboard



async def keyboard_inputs(websocket):
    while True:
        key = await asyncio.to_thread(keyboard.read_key)
        if key == "w":
            await websocket.send("MOVE N")
        elif key == "s":    
            await websocket.send("MOVE S")
        elif key == "a":
            await websocket.send("MOVE W")
        elif key == "d":
            await websocket.send("MOVE E")
        elif key == "p":
            await websocket.send("POS ")
        elif key == "esc":
            await websocket.send("EXIT")

# Function to receive messages from the server
async def receive_messages(websocket):
    while True:
        # Wait for a message from the server
        message = await websocket.recv()
        print(f"{message}")

# Function to send user input to the server
async def send_input(websocket):
    while True:
        # Use aioconsole to handle async input without blocking
        message = await aioconsole.ainput("")

        if message.lower() == "exit":
            print("Closing connection...")
            await websocket.close()
            break

        # Send the typed message to the server
        await websocket.send(message)

async def connect():
    name = input("What's your name? ")
    uri = "ws://137.112.215.152:8000/ws/" + name
    async with websockets.connect(uri) as websocket:
        print("Connected to server!")

        # Run both tasks concurrently: one for receiving and one for sending
        await asyncio.gather(
            receive_messages(websocket),  # This task will keep listening for server messages
            send_input(websocket),     # This task will handle user input and sending
            keyboard_inputs(websocket)
        )

# Start the WebSocket client and establish the connection
asyncio.run(connect())