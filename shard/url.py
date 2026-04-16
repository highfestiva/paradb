import os
import socket


SHARD_SERVICE_PORT = int(os.environ.get("SHARD_SERVICE_PORT", "3357"))


def get_host_url():
    return f"http://{socket.gethostname()}:{SHARD_SERVICE_PORT}"
