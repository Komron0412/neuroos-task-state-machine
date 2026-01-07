from django.db import transaction, IntegrityError
from .models import Task, TaskHold
from .state_machine import TaskStateMachine
from .models import TaskState


class TaskHoldAlreadyExists(Exception):
    pass


@transaction.atomic
def take_task(task_id: int, user):
    task = (
        Task.objects
        .select_for_update()
        .get(id=task_id)
    )

    if task.owner is not None:
        raise TaskHoldAlreadyExists("Task already taken")

    TaskHold.objects.create(task=task)

    task.owner = user
    TaskStateMachine.transition(task, TaskState.RUNNING)

    task.save(update_fields=["owner", "state"])
    return task