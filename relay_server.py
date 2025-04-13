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

    # Start WebSocket server asynchronously
    await ws_server

    # Start the HTTP server (aiohttp) without blocking
    return web.AppRunner(app).setup()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()  # Get the current event loop
    loop.run_until_complete(main())  # Run the main function in the current event loop
    loop.run_forever()  # Keep the loop running to allow WebSocket and HTTP servers to continue running
