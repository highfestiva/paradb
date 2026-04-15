from .app import app, SHARD_SERVICE_PORT  # noqa: F401

import uvicorn

uvicorn.run(app, host="0.0.0.0", port=SHARD_SERVICE_PORT)
