import pytest
from tasks.models import Task, TaskHold, TaskState
from tasks.services import take_task, TaskHoldAlreadyExists


@pytest.mark.django_db(transaction=True)
def test_take_task_creates_hold_and_moves_state():
    task = Task.objects.create(title="service test")

    take_task(task.id)

    task.refresh_from_db()
    assert task.state == TaskState.RUNNING
    assert TaskHold.objects.filter(task=task).exists()


@pytest.mark.django_db(transaction=True)
def test_take_task_only_once():
    task = Task.objects.create(title="service test")

    take_task(task.id)

    with pytest.raises(TaskHoldAlreadyExists):
        take_task(task.id)