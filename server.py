import re

from fastapi import FastAPI, WebSocket
from typing import List, Dict
import json

app = FastAPI()
active_connections: Dict[str, WebSocket] = {}
player_pos: Dict[str, tuple] = {}

@app.websocket("/ws/{UserID}")
async def websocket_endpoint(websocket: WebSocket, UserID: str):
    await websocket.accept()
    active_connections[UserID] = websocket  # Store client connection
    #active_connections.append(websocket)
    print(f"Client {UserID} connected")
    player_pos[UserID] = (0, 0)
    try:
        while True:
            data = await websocket.receive_text()  # Receive message from client
            if data.startswith("MOVE"):
                if " N" in data:
                    player_pos[UserID] = (player_pos[UserID][0], player_pos[UserID][1]-1)
                    print(f"{UserID} moved north to {player_pos[UserID]}")
                elif " S" in data:
                    player_pos[UserID] = (player_pos[UserID][0], player_pos[UserID][1]+1)
                    print(f"{UserID} moved south to {player_pos[UserID]}")
                elif " E" in data:
                    player_pos[UserID] = (player_pos[UserID][0]+1, player_pos[UserID][1])
                    print(f"{UserID} moved east to {player_pos[UserID]}")
                elif " W" in data:
                    player_pos[UserID] = (player_pos[UserID][0]-1, player_pos[UserID][1])
                    print(f"{UserID} moved west to {player_pos[UserID]}")
            elif data.startswith("POS "):
                extra, target_user = data.split()
                target_user = target_user.strip()
                if target_user not in player_pos:
                    target_user = UserID
                print(f"Player {target_user} is at {player_pos[target_user]}")
                await active_connections[UserID].send_text(f"Player {target_user} is at {player_pos[target_user]}")
            else:
                print(f"User {UserID} said", data)  # Print to server console
                for uid, client in active_connections.items():
                    await client.send_text(data)

            
            # Broadcast to all clients
            #for connection in active_connections:
            #    await connection.send_text(data)
    except:
        del active_connections[UserID]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="137.112.213.234", port=8000)
