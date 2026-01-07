from django.db import transaction, IntegrityError
from .models import Task, TaskHold
from .state_machine import TaskStateMachine
from .models import TaskState


class TaskHoldAlreadyExists(Exception):
    pass


@transaction.atomic
def take_task(task_id: int):
    """
    Atomically:
    - lock task row
    - create task_hold only once
    - move task to RUNNING
    """

    task = (
        Task.objects
        .select_for_update()
        .get(id=task_id)
    )

    try:
        TaskHold.objects.create(task=task)
    except IntegrityError:
        raise TaskHoldAlreadyExists(f"Task {task_id} already taken")

    TaskStateMachine.transition(task, TaskState.RUNNING)

    return task