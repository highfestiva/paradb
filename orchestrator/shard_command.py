from .shards import Shard


class ShardCommand:
    def __init__(self, shard: Shard):
        self.shard = shard

    def halt_flush_partition_writes(self, partition_index: int):
        pass

    def send_partitions(self):
        pass


class ShardBroadcastCommand:
    def __init__(self, shards: list[Shard]):
        self.shards = shards

    def send_partitions(self):
        for shard in self.shards:
            ShardCommand(shard).send_partitions()
