# ParaDB: a simple, parallel document db with separate storage and compute

This is a slow DB for education purposes only. Mostly for mine, I wrote it to learn how parallel DBs work.

## Architecture

This runs in minikube. The DB is written in Python, has a single orchestrator and a number of dynamic shards. The
storage is separate, and scale-to-zero would be possible to implement fairly easily, but the orchestrator would still
need to be running. The shards scales horizontally in a linear fasion.

Each shard is responsible for a number of partitions, for which it can write documents. To determine to which partition
a document belongs, some bits in its document ID is used. A shard that receives a write for a document, that belongs to
a partition for which it does not have write permission, will forward that write to the owning shard.

*Some graph...*

## Start the ParaDB in minikube

```bash
...
```

### Running tests

```bash
...
```
