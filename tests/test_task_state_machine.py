import pytest

from neuroos_app.models.task import Task
from neuroos_app.services.task_state_machine import validate_transition


def test_executor_can_take_task():
    task = Task(id=1, state="available")
    actor = {"id": 10, "role": "EXECUTOR"}

    validate_transition(task, "in_progress", actor)


def test_executor_cannot_finish_task_directly():
    task = Task(id=1, state="available")
    actor = {"id": 10, "role": "EXECUTOR"}

    with pytest.raises(ValueError):
        validate_transition(task, "done", actor)


def test_executor_cannot_cancel_task():
    task = Task(id=1, state="in_progress")
    actor = {"id": 10, "role": "EXECUTOR"}

    with pytest.raises(ValueError):
        validate_transition(task, "cancelled", actor)


def test_admin_can_approve_task():
    task = Task(id=1, state="review")
    actor = {"id": 1, "role": "ADMIN"}

    validate_transition(task, "done", actor)


def test_cannot_transition_from_done():
    task = Task(id=1, state="done")
    actor = {"id": 1, "role": "ADMIN"}

    with pytest.raises(ValueError):
        validate_transition(task, "review", actor)