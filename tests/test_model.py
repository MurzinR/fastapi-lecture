import datetime
from uuid import UUID

import pytest as pytest
from pydantic import ValidationError

from src.model import Task, TaskTrace, TaskStatus


@pytest.mark.parametrize(
    'model, params, exp_obj',
    [
        (
                Task,
                {
                    'id': UUID(int=0),
                    'timeout': 2.8,
                },
                Task(
                    id=UUID(int=0),
                    timeout=2.8,
                ),
        ),

        (
                TaskTrace,
                {
                'task_id': UUID(int=1),
                'ts': datetime.datetime(2021, 12, 17),
                'status': TaskStatus.DRAFT,
                'user_message': 'hi, user',
                'developer_message': 'hi, developer',
            },
                TaskTrace(
                task_id=UUID(int=1),
                ts=datetime.datetime(2021, 12, 17),
                status=TaskStatus.DRAFT,
                user_message='hi, user',
                developer_message='hi, developer',
            )
        ),
    ]
)
def test_creating_model(model, params, exp_obj):
    obj = model(**params)

    assert obj == exp_obj


@pytest.mark.parametrize(
    'model, params',
    [
        (
                Task,
                {
                    'id': 1,
                    'timeout': 2.8,
                },
        ),
    ]
)
def test_cannot_create_model(model, params):
    with pytest.raises(ValidationError):
        model(**params)
