import socket
import threading
import time
import os
import yaml
from datetime import datetime, timezone

# --- CONFIG LOADING ---
def load_config(file_path="settings.yaml"):
    if not os.path.exists(file_path):
        # If config missing, create a default one
        default = {
            "node_id": "Node-5005",
            "host": "127.0.0.1",
            "port": 5005,
            "peer_host": "127.0.0.1",
            "peer_port": 5006,
            "heartbeat_interval": 5,
            "backup_interval": 3600,
        }
        with open(file_path, "w") as f:
            yaml.dump(default, f)
        return default
    else:
        with open(file_path, "r") as f:
            return yaml.safe_load(f)

# --- MEMORY BUFFER ---
memory_buffer = []

def listener(host, port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        data = conn.recv(4096)
        if data:
            memory_buffer.append(data)
        conn.close()

def sync_to_peer(peer_host, peer_port):
    while True:
        if memory_buffer:
            memory = memory_buffer.pop(0)
            try:
                client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                client.connect((peer_host, peer_port))
                client.sendall(memory)
                client.close()
            except Exception as e:
                print(f"⚠️ Sync error: {e}")
        time.sleep(2)

# --- MAIN ---
import argparse
parser = argparse.ArgumentParser()
parser.add_argument("--config", type=str, default="settings.yaml", help="Config file path")
args = parser.parse_args()

cfg = load_config(args.config)

NODE_ID = cfg["node_id"]
LISTEN_HOST = cfg["host"]
LISTEN_PORT = cfg["port"]
PEER_HOST = cfg["peer_host"]
PEER_PORT = cfg["peer_port"]
HEARTBEAT_INTERVAL = cfg["heartbeat_interval"]

print(f"✅ {NODE_ID} is live! Listening {LISTEN_HOST}:{LISTEN_PORT}, syncing to {PEER_HOST}:{PEER_PORT}")

# --- THREADS ---
threading.Thread(target=listener, args=(LISTEN_HOST, LISTEN_PORT), daemon=True).start()
threading.Thread(target=sync_to_peer, args=(PEER_HOST, PEER_PORT), daemon=True).start()

while True:
    print(f"💓 {datetime.now(timezone.utc).isoformat()} - Heartbeat (memory size: {len(memory_buffer)})")
    time.sleep(HEARTBEAT_INTERVAL)
