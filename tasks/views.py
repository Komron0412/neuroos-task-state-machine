from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .models import Task, TaskState
from .serializers import TaskSerializer
from .services import take_task, TaskHoldAlreadyExists
from .state_machine import TaskStateMachine, InvalidTaskTransition


class TakeTaskAPIView(APIView):
    def post(self, request, task_id):
        try:
            task = take_task(task_id)
        except Task.DoesNotExist:
            return Response(
                {"detail": "Task not found"},
                status=status.HTTP_404_NOT_FOUND,
            )
        except TaskHoldAlreadyExists as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_409_CONFLICT,
            )

        return Response(
            TaskSerializer(task).data,
            status=status.HTTP_200_OK,
        )


class CompleteTaskAPIView(APIView):
    def post(self, request, task_id):
        try:
            task = Task.objects.get(id=task_id)
            TaskStateMachine.transition(task, TaskState.DONE)
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