import datetime
from uuid import UUID

from ...model import TaskTrace, TaskStatus
from ...services.solver import SolverProtocol
from ...services.storage import StorageProtocol


class Worker:
    def __init__(self, storage: StorageProtocol, solver: SolverProtocol):
        self._storage = storage
        self._solver = solver

    def handle_task(self, task_id: UUID):
        self._storage.save_task_trace(
            TaskTrace(
                task_id=task_id,
                ts=datetime.datetime.utcnow(),
                status=TaskStatus.SENT,
                user_message='Задача забрана из очереди',
                developer_message='Задача забрана из очереди',
            )
        )

        task = self._storage.load_task(task_id)

        self._storage.save_task_trace(
            TaskTrace(
                task_id=task_id,
                ts=datetime.datetime.utcnow(),
                status=TaskStatus.SOLVING,
                user_message='Задача решается',
                developer_message='Задача решается',
            )
        )
        self._solver.solve_task(task)
        self._storage.save_task_trace(
            TaskTrace(
                task_id=task_id,
                ts=datetime.datetime.utcnow(),
                status=TaskStatus.SOLVED,
                user_message='Задача решена',
                developer_message='Задача решена',
            )
        )
