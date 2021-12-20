import asyncio
import datetime
from http import HTTPStatus
from uuid import UUID

from fastapi import FastAPI
from starlette.websockets import WebSocket

from ...model import TaskStatus, Task, TaskTrace
from ...services.runner import TaskRunnerProtocol
from ...services.storage import StorageProtocol


def config_endpoints(
        app: FastAPI,
        storage: StorageProtocol,
        task_runner: TaskRunnerProtocol,
) -> FastAPI:

    @app.post(
        '/tasks',
        status_code=HTTPStatus.CREATED,
        response_model=TaskTrace,
    )
    async def create_task(task: Task) -> TaskTrace:
        storage.save_task(task)
        task_trace = TaskTrace(
            task_id=task.id,
            ts=datetime.datetime.utcnow(),
            status=TaskStatus.DRAFT,
            user_message='Задача создана',
            developer_message='Задача создана',
        )
        storage.save_task_trace(task_trace)

        task_runner.run_task(task.id)

        return task_trace

    @app.get(
        '/traces',
        status_code=HTTPStatus.OK,
        response_model=TaskTrace,
    )
    async def read_last_trace(task_id: UUID) -> TaskTrace:
        last_task_trace = storage.load_last_task_trace(task_id)
        return last_task_trace

    @app.websocket('/task_traces/{task_id}')
    async def get_task_traces(websocket: WebSocket):
        await websocket.accept()
        try:
            task_id = UUID(hex=websocket.path_params.get('task_id'))
            while True:
                trace = storage.load_last_task_trace(task_id)
                await websocket.send_text(trace.json())
                if trace.status is TaskStatus.SOLVED:
                    await websocket.close()
                await asyncio.sleep(1)
        except Exception as exp:
            await websocket.send_json({'WebSocketError': (type(exp).__name__, str(exp))})
        finally:
            await websocket.close()

    return app
