TERMINAL_STATES = {"done", "rejected", "cancelled"}

ALLOWED_TRANSITIONS = {
    "available": {
        "in_progress": ["EXECUTOR"],
        "cancelled": ["ADMIN", "SYSTEM"],
    },
    "in_progress": {
        "review": ["EXECUTOR"],
        "cancelled": ["ADMIN", "SYSTEM"],
    },
    "review": {
        "done": ["ADMIN"],
        "rejected": ["ADMIN"],
        "cancelled": ["ADMIN", "SYSTEM"],
    },
}


def validate_transition(task, new_state: str, actor: dict):
    # terminal state check
    if task.state in TERMINAL_STATES:
        raise ValueError("INVALID_STATE_TRANSITION")

    allowed_targets = ALLOWED_TRANSITIONS.get(task.state)
    if not allowed_targets:
        raise ValueError("INVALID_STATE_TRANSITION")

    allowed_roles = allowed_targets.get(new_state)
    if not allowed_roles:
        raise ValueError("INVALID_STATE_TRANSITION")

    if actor["role"] not in allowed_roles:
        raise ValueError("INVALID_STATE_TRANSITION")

    # executor-specific rules
    if actor["role"] == "EXECUTOR":
        if new_state == "review" and task.executor_id != actor["id"]:
            raise ValueError("INVALID_STATE_TRANSITION")