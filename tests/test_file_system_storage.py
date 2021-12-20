import datetime
from uuid import UUID

from src.model import Task, TaskTrace, TaskStatus


def test_storing_task(file_system_storage):
    task = Task(id=UUID(int=1), timeout=10)

    file_system_storage.save_task(task)
    loaded_task = file_system_storage.load_task(task.id)

    assert loaded_task == task


def test_storing_traces(file_system_storage):
    task = Task(id=UUID(int=1), timeout=10)
    trace_1 = TaskTrace(
        task_id=task.id,
        ts=datetime.datetime.utcnow(),
        status=TaskStatus.DRAFT,
        user_message='',
        developer_message='',
    )
    trace_2 = TaskTrace(
        task_id=task.id,
        ts=datetime.datetime.utcnow(),
        status=TaskStatus.DRAFT,
        user_message='',
        developer_message='',
    )

    file_system_storage.save_task(task)
    file_system_storage.save_task_trace(trace_1)
    file_system_storage.save_task_trace(trace_2)
    loaded_traces = file_system_storage.load_task_traces(task.id)

    assert loaded_traces == [trace_1, trace_2]


def test_loading_last_trace(file_system_storage):
    task = Task(id=UUID(int=1), timeout=10)
    trace_1 = TaskTrace(
        task_id=task.id,
        ts=datetime.datetime.utcnow(),
        status=TaskStatus.DRAFT,
        user_message='',
        developer_message='',
    )
    trace_2 = TaskTrace(
        task_id=task.id,
        ts=datetime.datetime.utcnow(),
        status=TaskStatus.DRAFT,
        user_message='',
        developer_message='',
    )

    file_system_storage.save_task(task)
    file_system_storage.save_task_trace(trace_1)
    file_system_storage.save_task_trace(trace_2)
    loaded_trace = file_system_storage.load_last_task_trace(task.id)

    assert loaded_trace == trace_2
