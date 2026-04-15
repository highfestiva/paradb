from shared.types.partition_bits import PARTITION_INDEXES


class Partition:
    def __init__(self, index):
        self.index: int = index
        self.owner: str = ''

    def release(self):
        self.owner = ''


INDEX_TO_PARTITION = {}


def init():
    global INDEX_TO_PARTITION
    INDEX_TO_PARTITION = {pi: Partition(pi) for pi in PARTITION_INDEXES}


def get_free_partitions():
    for partition in INDEX_TO_PARTITION.values():
        if not partition.owner:
            yield partition
