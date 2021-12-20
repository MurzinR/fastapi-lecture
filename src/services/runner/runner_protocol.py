import abc
from uuid import UUID

from typing_extensions import Protocol


class TaskRunnerProtocol(Protocol):

    @abc.abstractmethod
    def run_task(self, task_id: UUID):
        pass
