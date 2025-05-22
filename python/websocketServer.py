import websockets
import asyncio

host = "127.0.0.1"
port = 64510

async def handle_client(websockets):
    print("client connecté")
    try:
        async for message in websockets:
            print(f"message recus: {message}")
    except websockets.ConnectionClosed:
        print("connexion clos")

async def main():
    #creer et demare le server
    async with websockets.serve(handle_client, host, port):
        print("le serveur écoute")
        await asyncio.Future() #le maintient actif

#lance main
if __name__ == "__main__":
    asyncio.run(main())