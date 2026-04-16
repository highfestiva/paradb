from pydantic import BaseModel


class ShardInfo(BaseModel):
    url: str
    load: float


class ShardPartitionInfo(ShardInfo):
    partitions: list[int]
