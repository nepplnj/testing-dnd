import re
import pandas

from fastapi import FastAPI, WebSocket
from typing import Dict

app = FastAPI()
active_connections: Dict[str, WebSocket] = {}
player_pos: Dict[str, tuple] = {}
map = 'checkmap.xlsx'
spn = [0,0]
df = pandas.read_excel(map,header=None)
matrix = df.values.tolist()

@app.websocket("/ws/{UserID}")
async def websocket_endpoint(websocket: WebSocket, UserID: str):
    await websocket.accept()
    active_connections[UserID] = websocket  # Store client connection
    #active_connections.append(websocket)
    print(f"Client {UserID} connected")
    for uid, client in active_connections.items():
        await client.send_text(f"JOIN {UserID} {spn}")
    player_pos[UserID] = spn
    global matrix
    await active_connections[UserID].send_text(f"MAP {matrix}")
    try:
        while True:
            data = await websocket.receive_text()  # Receive message from client
            if data.startswith("MOVE"):
                if " N" in data:
                    player_pos[UserID] = (player_pos[UserID][0], player_pos[UserID][1]-1)
                    print(f"{UserID} moved north to {player_pos[UserID]}")
                    for uid, client in active_connections.items():
                        await client.send_text(f"LOC {UserID} {player_pos[UserID]}")
                elif " S" in data:
                    player_pos[UserID] = (player_pos[UserID][0], player_pos[UserID][1]+1)
                    print(f"{UserID} moved south to {player_pos[UserID]}")
                    for uid, client in active_connections.items():
                        await client.send_text(f"LOC {UserID} {player_pos[UserID]}")
                elif " E" in data:
                    player_pos[UserID] = (player_pos[UserID][0]+1, player_pos[UserID][1])
                    print(f"{UserID} moved east to {player_pos[UserID]}")
                    for uid, client in active_connections.items():
                        await client.send_text(f"LOC {UserID} {player_pos[UserID]}")
                elif " W" in data:
                    player_pos[UserID] = (player_pos[UserID][0]-1, player_pos[UserID][1])
                    print(f"{UserID} moved west to {player_pos[UserID]}")
                    for uid, client in active_connections.items():
                        await client.send_text(f"LOC {UserID} {player_pos[UserID]}")
            elif data.startswith("POS "):
                extra, target_user = data.split()
                target_user = target_user.strip()
                if target_user not in player_pos:
                    target_user = UserID
                print(f"Player {target_user} is at {player_pos[target_user]}")
                await active_connections[UserID].send_text(f"Player {target_user} is at {player_pos[target_user]}")
            elif data == "REFRESH":
                global map
                df = pandas.read_excel(map,header=None)
                matrix = df.values.tolist()
                for uid, client in active_connections.items():
                    await client.send_text(f"MAP {matrix}")
            elif data.startswith("SETMAP"):
                extra, mapname = data.split()
                map = mapname + ".xlsx"
            else:
                print(f"User {UserID} said", data)  # Print to server console
                for uid, client in active_connections.items():
                    await client.send_text(data)

            
            # Broadcast to all clients
            #for connection in active_connections:
            #    await connection.send_text(data)
    except:
        for uid, client in active_connections.items():
            await client.send_text(f"LEAVE {UserID}")
        del active_connections[UserID]

if __name__ == "__main__":
    import uvicorn
    ip = input("Host IPv4: ")
    uvicorn.run(app, host=ip, port=8000)
