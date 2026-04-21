import os
import socket


HOSTNAME = os.environ.get("POD_IP", socket.gethostname())
SHARD_SERVICE_PORT = int(os.environ.get("SHARD_SERVICE_PORT", "3357"))


def get_host_url():
    return f"http://{HOSTNAME}:{SHARD_SERVICE_PORT}"
