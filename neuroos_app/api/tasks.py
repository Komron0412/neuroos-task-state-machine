from fastapi import APIRouter, HTTPException
from neuroos_app.models.task import Task
from neuroos_app.services.task_state_machine import validate_transition

router = APIRouter()

FAKE_TASK = Task(id=1, state="available")

FAKE_ACTOR = {
    "id": 10,
    "role": "EXECUTOR"
}

@router.post("/tasks/{task_id}/state")
def change_state(task_id: int, new_state: str):
    try:
        validate_transition(FAKE_TASK, new_state, FAKE_ACTOR)
        FAKE_TASK.state = new_state
        return {"task_id": task_id, "new_state": new_state}
    except ValueError:
        raise HTTPException(status_code=409, detail="INVALID_STATE_TRANSITION")