from .models import TaskState


class InvalidTaskTransition(Exception):
    pass


class TaskStateMachine:
    """
    Task state transition rules
    """

    transitions = {
        TaskState.PENDING: {TaskState.RUNNING},
        TaskState.RUNNING: {TaskState.DONE, TaskState.FAILED},
        TaskState.DONE: set(),
        TaskState.FAILED: set(),
    }

    @classmethod
    def can_transition(cls, from_state: str, to_state: str) -> bool:
        return to_state in cls.transitions.get(from_state, set())

    @classmethod
    def transition(cls, task, to_state: str):
        if not cls.can_transition(task.state, to_state):
            raise InvalidTaskTransition(
                f"Invalid transition: {task.state} → {to_state}"
            )

        task.state = to_state
        task.save(update_fields=["state"])
        return task