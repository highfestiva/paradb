#!/usr/bin/env python3

from fastapi import FastAPI

from .balancer import balance_shards
from .partitions import get_free_partitions
from .shards import all_shards, fetch_shard, release_shard
from .shard_command import ShardCommand
from shared.types.shard import ShardInfo, ShardPartitionInfo


app = FastAPI()


@app.post("/shard")
def update_shard(shard_info: ShardInfo):
    shard = fetch_shard(shard_info)
    free_partitions = list(get_free_partitions())
    shard.add_partitions(free_partitions)
    if free_partitions:
        ShardCommand(shard).send_partitions()
    balance_shards()
    return {"status": 0}


@app.delete("/shard")
def delete_shard(url: str):
    release_shard(url)
    return {"status": 0}


@app.get("/shard")
def get_shards():
    shards = []
    for shard in all_shards():
        pis = [p.index for p in shard.partitions]
        shard_partitions = ShardPartitionInfo.model_construct(url=shard.url, load=shard.load, partitions=pis)
        shards.append(shard_partitions)
    return {'status': 0, 'shards': shards}
