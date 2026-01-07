import pytest
from tasks.models import Task, TaskState
from tasks.state_machine import TaskStateMachine, InvalidTaskTransition


@pytest.mark.django_db
def test_valid_transitions():
    task = Task.objects.create(title="test")

    TaskStateMachine.transition(task, TaskState.RUNNING)
    assert task.state == TaskState.RUNNING

    TaskStateMachine.transition(task, TaskState.DONE)
    assert task.state == TaskState.DONE


@pytest.mark.django_db
def test_invalid_transition():
    task = Task.objects.create(title="test")

    with pytest.raises(InvalidTaskTransition):
        TaskStateMachine.transition(task, TaskState.DONE)