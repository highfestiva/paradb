from .shards import all_shards
from .shard_command import ShardCommand, ShardBroadcastCommand
from shared.try_lock import TryLock


try_lock = TryLock()


def balance_shards():
    """Balance so each shard have equal number of partitions."""

    # only one thread at a time
    with try_lock as locked:
        if not locked:
            return

        # sort based on how many partitions they each have
        shards_balance = sorted(all_shards(), key=lambda sh: len(sh.partitions))
        # check if we move a partition
        if shards_balance and len(shards_balance[0].partitions) <= len(shards_balance[-1].partitions) - 2:
            # yep, move partition
            smallest = shards_balance[0]
            biggest = shards_balance[-1]
            partition = biggest.partitions[-1]
            # stop writes from this shard
            ShardCommand(biggest).halt_flush_partition_writes(partition.index)
            biggest.remove_partition(partition)
            smallest.add_partitions([partition])
            # enable writes from all other shards, and finally
            ShardBroadcastCommand(shards_balance).send_partitions()
