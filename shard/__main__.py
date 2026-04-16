from .app import app
from .url import SHARD_SERVICE_PORT

import uvicorn

uvicorn.run(app, host="0.0.0.0", port=SHARD_SERVICE_PORT)
