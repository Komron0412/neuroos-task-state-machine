# NeuroOS – Task State Machine

This repository implements **Section 10 – Task State Machine** of the NeuroOS backend specification.

The goal of this module is to strictly enforce **task state transitions**, **role-based access rules**, and to block any invalid transitions.

---

## Task State Machine Rules

Allowed transitions:

| From        | To          | Who            |
|-------------|-------------|----------------|
| available   | in_progress | EXECUTOR       |
| in_progress | review      | EXECUTOR       |
| review      | done        | ADMIN          |
| review      | rejected    | ADMIN          |
| available   | cancelled   | ADMIN / SYSTEM |
| in_progress | cancelled   | ADMIN / SYSTEM |
| review      | cancelled   | ADMIN / SYSTEM |

Any other transition results in:

INVALID_STATE_TRANSITION (HTTP 409)

Terminal states:
- `done`
- `rejected`
- `cancelled`

---

## Implementation Highlights

- State validation implemented in the **service layer**
- Role-based transition checks
- Terminal states cannot be transitioned from
- Invalid transitions are rejected consistently
- Business logic covered by **unit tests (pytest)**


## Run Locally

Requirements:
- Python **3.11**

```bash
python3.11 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn neuroos_app.main:app --reload

API documentation:

http://127.0.0.1:8000/docs


⸻

Run Tests

pytest -v


⸻

Scope Notes

This repository intentionally covers only the Task State Machine.
Authentication, database persistence, and financial logic are outside the scope of this module.

⸻

Status: Section 10 – Task State Machine COMPLETED ✅

