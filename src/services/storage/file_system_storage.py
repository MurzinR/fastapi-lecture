from pathlib import Path
from typing import List, Dict
from uuid import UUID, uuid4

from .storage_protocol import StorageProtocol
from ...model import Task, TaskTrace


class FileSystemStorage(StorageProtocol):
    """
    Хранилище на файловой системе
    """

    TASK_DIR = 'tasks'
    TASK_FILENAME_TEMPLATE = 'TASK.json'
    TASK_TRACE_FILENAME_TEMPLATE = 'TASK_TRACE_%s.json'
    TASK_TRACE_FILENAME_WILDCARD = 'TASK_TRACE_*.json'

    def __init__(self, dir_path: Path):
        self._rocket_dir = dir_path / self.TASK_DIR
        self._rocket_dir.mkdir(exist_ok=True)

    def _get_task_dir(self, task_id: UUID) -> Path:
        task_dir = self._rocket_dir / str(task_id)
        task_dir.mkdir(exist_ok=True, parents=True)
        return task_dir

    def _get_task_filepath(self, task_id: UUID) -> Path:
        rocket_dir = self._get_task_dir(task_id)
        return rocket_dir / self.TASK_FILENAME_TEMPLATE

    def save_task(self, task: Task):
        # language=rst
        """
        Сохранить задачу.

        :param task: Задача
        :return:
        """
        rocket_filepath = self._get_task_filepath(task.id)
        rocket_filepath.write_text(task.json())

    def load_task(self, task_id: UUID) -> Task:
        # language=rst
        """
        Загрузить задачу.

        :param task_id: ID задачи.
        :return: Задача.
        """
        rocket_filepath = self._get_task_filepath(task_id)
        rocket = Task.parse_file(rocket_filepath)

        return rocket

    def save_task_trace(self, task_trace: TaskTrace):
        rocket_dir = self._get_task_dir(task_trace.task_id)
        rocket_trace_filename = self.TASK_TRACE_FILENAME_TEMPLATE % uuid4()
        rocket_trace_filepath = rocket_dir / rocket_trace_filename
        rocket_trace_filepath.write_text(task_trace.json())

    def load_task_traces(self, task_id: UUID) -> List[TaskTrace]:
        task_dir = self._get_task_dir(task_id)
        task_traces = [
            TaskTrace.parse_file(filepath) for filepath in task_dir.glob(self.TASK_TRACE_FILENAME_WILDCARD)
        ]

        task_traces.sort(key=lambda trace: trace.ts)

        return task_traces

    def load_last_task_trace(self, task_id: UUID) -> TaskTrace:
        task_traces = self.load_task_traces(task_id)
        last_task_trace = task_traces[-1]

        return last_task_trace
