from pathlib import Path

from src.components.rest import init_app
from src.components.worker.worker import Worker
from src.services.runner import SimpleTaskRunner
from src.services.solver import Solver
from src.services.storage import FileSystemStorage

app_dir = Path('app_folder')
app_dir.mkdir(parents=True, exist_ok=True)
storage = FileSystemStorage(app_dir)

solver = Solver()
worker = Worker(storage, solver)
task_runner = SimpleTaskRunner(worker)

app = init_app(storage, task_runner)
