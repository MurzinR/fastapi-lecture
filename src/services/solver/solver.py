import time

from ...model import Task
from .solver_protocol import SolverProtocol


class Solver(SolverProtocol):
    def solve_task(self, task: Task):
        time.sleep(task.timeout)
