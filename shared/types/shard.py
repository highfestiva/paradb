from pydantic import BaseModel


class ShardInfo(BaseModel):
    hostname: str
    load: float


class ShardPartitionInfo(ShardInfo):
    partitions: list[int]
