class Task:
    def __init__(self, id: int, state: str, executor_id: int | None = None):
        self.id = id
        self.state = state
        self.executor_id = executor_id