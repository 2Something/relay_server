import asyncio
import websockets
import os
from aiohttp import web

clients = set()

# WebSocket handler
async def relay(websocket, path):
    print("New client connected.")
    clients.add(websocket)
    try:
        async for message in websocket:
            # Broadcast to other clients
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except:
        pass
    finally:
        clients.remove(websocket)
        print("Client disconnected.")

# HTTP health check
async def health_check(request):
    return web.Response(text="OK")

async def main():
    port = int(os.environ.get("PORT", 10000))  # Render provides PORT

    # Create an aiohttp application and add the health check route
    app = web.Application()
    app.router.add_get('/health', health_check)

    # WebSocket server
    ws_server = websockets.serve(relay, "0.0.0.0", port)

    # Await the WebSocket server directly
    await ws_server

    # Start the HTTP server (aiohttp)
    await web.run_app(app, port=port)  # Await the web server

if __name__ == "__main__":
    asyncio.run(main())  # Correctly await the main coroutine
