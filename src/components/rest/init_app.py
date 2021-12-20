from fastapi import FastAPI

from .endpoints import config_endpoints
from ...services.runner import TaskRunnerProtocol
from ...services.storage import StorageProtocol


def init_app(
        storage: StorageProtocol,
        runner: TaskRunnerProtocol,
) -> FastAPI:
    app = FastAPI()

    config_endpoints(app, storage, runner)

    return app
