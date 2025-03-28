import asyncio
import websockets
import pygame
from typing import Dict


def refresh():  # Function to refresh the grid map
    global matrix
    for i in range(round(xlen/dist)):
        for j in range(round(ylen/dist)):
                pygame.draw.rect(screen, colors[matrix[i][j]], (j*dist, i*dist, dist, dist))
    for uid, pos in player_pos.items():
        pygame.draw.rect(screen, red, (pos[0]*dist, pos[1]*dist, dist, dist))
    pygame.display.flip()

pygame.init()

player_pos: Dict[str, tuple] = {}


#define some vars
dist = 50
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
xlen = 800
ylen = 800
colors = [white, black, red, green, blue]
matrix = [[0 for _ in range(50)] for _ in range(50)]


async def keyboard_inputs(websocket):
    print("Open the python window!")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Handle window close
                await websocket.close()
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
                elif event.key == pygame.K_r:
                    refresh()
                elif event.key == pygame.K_ESCAPE:
                    await websocket.close()
                    pygame.quit()
                    return

        pygame.display.flip()
        await asyncio.sleep(0.01)  # Prevent CPU overuse



# Function to receive messages from the server
async def receive_messages(websocket):
    while True:
        # Wait for a message from the server
        message = await websocket.recv()
        if message.find("MAP") != -1:
            global matrix
            mat = message.split(' ',1)
            matrix = eval(mat[1])
            refresh()
        elif message.find("JOIN") != -1:
            temp = message.split(' ',2)
            player_pos[temp[1]] = eval(temp[2])
            refresh()
        elif message.find("LOC") != -1:
            temp = message.split(' ',2)
            player_pos[temp[1]] = eval(temp[2])
            refresh()
        print(f"{message}")

async def connect():
    name = input("What's your name? ")
    ip = input("Host IPv4: ")
    uri = "ws://" + ip + ":8000/ws/" + name
    player_pos[name] = (0,0)
    async with websockets.connect(uri) as websocket:
        print("Connected to server!")
        global screen
        screen = pygame.display.set_mode((xlen, ylen))
        pygame.display.set_caption("Grid Map")

        # Run both tasks concurrently: one for receiving and one for sending
        await asyncio.gather(
            receive_messages(websocket),
            keyboard_inputs(websocket)
        )

# Start the WebSocket client and establish the connection
asyncio.run(connect())