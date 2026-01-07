NeuroOS – Task State Machine (Django)

Production-ready task management backend built with Django & Django REST Framework.
This project demonstrates clean architecture, state machine logic, database-level invariants, JWT authentication, and full test coverage.

⸻

🚀 Features
	•	✅ Task state machine (pending → running → done / failed)
	•	🔒 DB-level invariant: task can be taken only once
	•	⚡ Transactional safety (select_for_update, atomic operations)
	•	🔐 JWT Authentication
	•	👤 Ownership-based permissions
	•	📡 REST API
	•	📘 Swagger / OpenAPI documentation
	•	🧪 Comprehensive tests (state, services, API)

⸻

🏗 Architecture Overview

The project follows Clean Architecture principles:

tasks/
├── models.py         # Data models + DB constraints
├── state_machine.py  # Pure business rules
├── services.py       # Atomic orchestration & invariants
├── permissions.py    # Custom access control
├── serializers.py    # API representation
├── views.py          # HTTP layer
├── urls.py
└── tests/            # Unit & integration tests

Why this architecture?
	•	Business logic is not coupled to HTTP or Django models
	•	Easy to test and extend
	•	Safe under concurrency
	•	Production-oriented design

⸻

🔁 Task Lifecycle

PENDING → RUNNING → DONE
                 ↘ FAILED

Rules:
	•	A task can be taken only once
	•	Only the owner can complete or fail a task
	•	Invalid transitions are rejected

⸻

🔐 Authentication & Permissions
	•	JWT authentication (djangorestframework-simplejwt)
	•	Only authenticated users can access APIs
	•	Only task owner can change task state after taking it

⸻

📡 API Endpoints

Auth

POST /api/token/
POST /api/token/refresh/

Tasks

POST /api/tasks/{id}/take/
POST /api/tasks/{id}/complete/
POST /api/tasks/{id}/fail/


⸻

📘 API Documentation (Swagger)

After running the server:

👉 /api/docs/ – Swagger UI
👉 /api/schema/ – OpenAPI schema

Supports JWT authorization directly in Swagger.

⸻

🧪 Tests
	•	State machine validation
	•	Transaction & invariant tests
	•	API behavior tests (HTTP level)

Run all tests:

python -m pytest

Example output:

collected 6 items
6 passed in 0.19s


⸻

⚙️ Tech Stack
	•	Python 3.11+
	•	Django
	•	Django REST Framework
	•	PostgreSQL / SQLite
	•	JWT (SimpleJWT)
	•	drf-spectacular (OpenAPI)
	•	pytest + pytest-django

⸻

🧩 Use Cases
	•	Task orchestration systems
	•	Workflow engines
	•	Job queues / schedulers
	•	Microservice task coordination
	•	Educational example of state machines + DB invariants

