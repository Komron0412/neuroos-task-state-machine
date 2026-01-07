from django.db import models


class TaskState(models.TextChoices):
    PENDING = "pending", "Pending"
    RUNNING = "running", "Running"
    DONE = "done", "Done"
    FAILED = "failed", "Failed"


class Task(models.Model):
    title = models.CharField(max_length=255)
    state = models.CharField(
        max_length=20,
        choices=TaskState.choices,
        default=TaskState.PENDING,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class TaskHold(models.Model):
    task = models.OneToOneField(
        Task,
        on_delete=models.CASCADE,
        related_name="hold",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["task"],
                name="unique_task_hold",
            )
        ]