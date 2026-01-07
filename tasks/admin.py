from django.contrib import admin
from .models import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "state", "created_at")
    list_filter = ("state",)
    search_fields = ("title",)