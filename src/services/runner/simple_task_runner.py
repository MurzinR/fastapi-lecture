from multiprocessing import Process
from uuid import UUID

from .runner_protocol import TaskRunnerProtocol
from ...components.worker.worker import Worker


class SimpleTaskRunner(TaskRunnerProtocol):
    def __init__(self, worker: Worker):
        self._worker = worker

    def run_task(self, task_id: UUID):
        process = Process(target=self._worker.handle_task, args=(task_id,))
        process.start()
