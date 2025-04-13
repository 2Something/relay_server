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

    # Start the HTTP server (aiohttp) properly
    runner = web.AppRunner(app)
    await runner.setup()  # Properly await the setup
    site = web.TCPSite(runner, '0.0.0.0', port)
    await site.start()  # Start the site

    print(f"Server started on port {port}")
    # Run the server indefinitely
    while True:
        await asyncio.sleep(3600)  # Keep running the server

# Main execution logic
if __name__ == "__main__":
    try:
        loop = asyncio.get_running_loop()  # Try to get the current running event loop
    except RuntimeError:
        loop = asyncio.new_event_loop()  # Create a new event loop if none exists
        asyncio.set_event_loop(loop)  # Set the newly created event loop as the current one

    loop.create_task(main())  # Run the main function as a task
    loop.run_forever()  # Keep the event loop running
