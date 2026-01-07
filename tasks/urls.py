from django.urls import path
from .views import (
    TakeTaskAPIView,
    CompleteTaskAPIView,
    FailTaskAPIView,
)

urlpatterns = [
    path("tasks/<int:task_id>/take/", TakeTaskAPIView.as_view()),
    path("tasks/<int:task_id>/complete/", CompleteTaskAPIView.as_view()),
    path("tasks/<int:task_id>/fail/", FailTaskAPIView.as_view()),
]