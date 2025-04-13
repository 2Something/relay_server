import asyncio
import websockets
import os
from aiohttp import web

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

async def health_check(request):
    return web.Response(text="OK")

async def main():
    # Set WebSocket server on the appropriate port
    port = int(os.environ.get("PORT", 10000))
    
    # Create an HTTP server for health checks
    app = web.Application()
    app.router.add_get('/health', health_check)
    
    # Run WebSocket server
    ws_server = websockets.serve(relay, "0.0.0.0", port)
    
    # Start HTTP server for health check
    web.run_app(app, port=port)

    print(f"Starting WebSocket relay server on port {port}")
    await ws_server

if __name__ == "__main__":
    asyncio.run(main())
