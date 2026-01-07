import pytest
from rest_framework.test import APIClient
from tasks.models import Task, TaskState


@pytest.mark.django_db
def test_take_task_api():
    client = APIClient()
    task = Task.objects.create(title="api test")

    response = client.post(f"/api/tasks/{task.id}/take/")
    assert response.status_code == 200

    task.refresh_from_db()
    assert task.state == TaskState.RUNNING


@pytest.mark.django_db
def test_take_task_twice_api():
    client = APIClient()
    task = Task.objects.create(title="api test")

    client.post(f"/api/tasks/{task.id}/take/")
    response = client.post(f"/api/tasks/{task.id}/take/")

    assert response.status_code == 409