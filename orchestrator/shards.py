from .partitions import Partition
from shared.types.shard import ShardInfo


class Shard:
    def __init__(self, hostname: str):
        self.hostname: str = hostname
        self.partitions: list[Partition] = []
        self.load: float = 0.0

    def add_partitions(self, partitions: list[Partition]):
        for partition in partitions:
            partition.owner = self.hostname
            self.partitions.append(partition)

    def remove_partition(self, partition: Partition):
        self.partitions.remove(partition)
        partition.owner = ""

    def release(self):
        for partition in self.partitions:
            partition.release()
        self.partitions.clear()
        self.load = 0.0


NAME_TO_SHARD: dict[str, Shard] = {}


def init():
    pass


def all_shards():
    return NAME_TO_SHARD.values()


def fetch_shard(shard_info: ShardInfo):
    shard = NAME_TO_SHARD.get(shard_info.hostname)
    if not shard:
        shard = NAME_TO_SHARD[shard_info.hostname] = Shard(shard_info.hostname)
    shard.load = shard_info.load
    return shard


def release_shard(name: str):
    shard = NAME_TO_SHARD.get(name)
    if shard:
        shard.release()
        del NAME_TO_SHARD[name]
