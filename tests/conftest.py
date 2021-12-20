import tempfile
from pathlib import Path

import pytest

from src.services.storage.file_system_storage import FileSystemStorage


@pytest.fixture
def file_system_storage() -> FileSystemStorage:
    with tempfile.TemporaryDirectory() as tmp_dir:
        storage = FileSystemStorage(Path(tmp_dir))
        yield storage
