import abc

from typing_extensions import Protocol

from ...model import Task


class SolverProtocol(Protocol):
    @abc.abstractmethod
    def solve_task(self, task: Task):
        pass
