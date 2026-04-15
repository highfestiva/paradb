#!/usr/bin/env python3

from contextlib import asynccontextmanager
from fastapi import FastAPI
import socket
import uvicorn

from .orchestrator_command import OrchestratorCommand
from shared.types.shard import ShardInfo, ShardPartitionInfo


app = FastAPI()
shards: list[ShardPartitionInfo] = []
partition_to_shard_host: dict[int, str] = {}


@app.delete('/cmd/partition')
def halt_flush_partition_writes(partition_index: int):
    pass
    return {'status': 0}


@app.post('/cmd/partitions')
def update_shards(shard_partition_infos: list[ShardPartitionInfo]):
    global shards
    shards = shard_partition_infos
    for shard in shard_partition_infos:
        for partition in shard.partitions:
            partition_to_shard_host[partition] = shard.hostname
    return {'status': 0}


@asynccontextmanager
async def lifespan(app: FastAPI):
    # setup = inform orchestrator
    hostname = socket.gethostname()
    shard_info = ShardInfo(hostname=hostname, load=0.0)
    OrchestratorCommand().update_shard(shard_info)

    yield  # yield until app done


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3357)
