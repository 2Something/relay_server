import socket
import threading

clients = []

def handle_client(conn, addr):
    print(f"[+] {addr} connected.")
    clients.append(conn)
    try:
        while True:
            data = conn.recv(4096)
            if not data:
                break
            # Forward data to other clients
            for c in clients:
                if c != conn:
                    c.sendall(data)
    except Exception as e:
        print(f"[!] {addr} error: {e}")
    finally:
        conn.close()
        clients.remove(conn)
        print(f"[-] {addr} disconnected.")

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", 10000))  # Relay port
    server.listen()
    print("[*] Relay server started on port 10000")

    while True:
        conn, addr = server.accept()
        threading.Thread(target=handle_client, args=(conn, addr)).start()

if __name__ == "__main__":
    start()
