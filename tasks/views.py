from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from .models import Task, TaskState
from .serializers import TaskSerializer
from .services import take_task, TaskHoldAlreadyExists
from .state_machine import TaskStateMachine, InvalidTaskTransition
from rest_framework.permissions import IsAuthenticated
from .permissions import IsTaskOwner



@extend_schema(
    summary="Take task",
    description="Atomically take a task. Only once.",
    responses={200: TaskSerializer},
)
class TakeTaskAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, task_id):
        task = take_task(task_id, request.user)
        return Response(TaskSerializer(task).data)
@extend_schema(
    summary="Complete task",
    description="Only task owner can complete task",
)
class CompleteTaskAPIView(APIView):
    permission_classes = [IsAuthenticated, IsTaskOwner]

    def post(self, request, task_id):
        task = Task.objects.get(id=task_id)
        self.check_object_permissions(request, task)

        TaskStateMachine.transition(task, TaskState.DONE)
        return Response(TaskSerializer(task).data)

@extend_schema(
    summary="Complete task",
    description="Only task owner can complete task",
)
class FailTaskAPIView(APIView):
    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            TaskStateMachine.transition(task, TaskState.FAILED)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except InvalidTaskTransition as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(TaskSerializer(task).data)