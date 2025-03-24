import asyncio
import websockets
import aioconsole  # Asynchronous console input
import pygame

pygame.init()


async def keyboard_inputs(websocket):
    print("Listening for key presses...")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close
                websocket.close()
                return  

            if event.type == pygame.KEYDOWN:  # Detect when a key is pressed
                if event.key == pygame.K_w:
                    await websocket.send("MOVE N")
                elif event.key == pygame.K_s:    
                    await websocket.send("MOVE S")
                elif event.key == pygame.K_a:
                    await websocket.send("MOVE W")
                elif event.key == pygame.K_d:
                    await websocket.send("MOVE E")
                elif event.key == pygame.K_p:
                    await websocket.send("POS a")
                elif event.key == pygame.K_ESCAPE:
                    websocket.close()
                    return

        pygame.display.flip()
        await asyncio.sleep(0.01)  # Prevent CPU overuse



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
    uri = "ws://137.112.213.234:8000/ws/" + name
    async with websockets.connect(uri) as websocket:
        print("Connected to server!")
        screen = pygame.display.set_mode((400, 300))

        # Run both tasks concurrently: one for receiving and one for sending
        await asyncio.gather(
            receive_messages(websocket),  # This task will keep listening for server messages
            #send_input(websocket),     # This task will handle user input and sending
            keyboard_inputs(websocket)
        )

# Start the WebSocket client and establish the connection
asyncio.run(connect())