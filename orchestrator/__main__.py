from .app import app  # noqa: F401
from .partitions import init as partitions_init
from .shards import init as shards_init

import uvicorn

partitions_init()
shards_init()
uvicorn.run(app, host="0.0.0.0", port=3356)
