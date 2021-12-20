import abc
from typing import List
from uuid import UUID

from typing_extensions import Protocol

from ...model import TaskTrace, Task


class StorageProtocol(Protocol):
    """
    Протокол хранилища
    """

    @abc.abstractmethod
    def save_task(self, task: Task):
        # language=rst
        """
        Сохранить задачу.

        :param task: Задача
        :return:
        """

    @abc.abstractmethod
    def load_task(self, task_id: UUID) -> Task:
        # language=rst
        """
        Загрузить ракету.

        :param task_id: ID задачи.
        :return: Задача.
        """

    @abc.abstractmethod
    def save_task_trace(self, task_trace: TaskTrace):
        pass

    @abc.abstractmethod
    def load_task_traces(self, task_id: UUID) -> List[TaskTrace]:
        pass

    @abc.abstractmethod
    def load_last_task_trace(self, task_id: UUID) -> TaskTrace:
        pass
