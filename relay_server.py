import asyncio
import websockets
import os

clients = set()

async def relay(websocket, path):
    print("New client connected.")
    clients.add(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except:
        pass
    finally:
        clients.remove(websocket)
        print("Client disconnected.")

async def main():
    port = int(os.environ.get("PORT", 10000))  # Render sets PORT env var
    print(f"Starting WebSocket relay server on port {port}")
    async with websockets.serve(relay, "0.0.0.0", port):
        await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())