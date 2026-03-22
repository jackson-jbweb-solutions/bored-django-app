from django.urls import path

from . import views

urlpatterns = [
    path("", views.task_list, name="task-list"),
    path("create/", views.task_create, name="task-create"),
    path("<int:pk>/edit/", views.task_edit, name="task-edit"),
    path("<int:pk>/row/", views.task_row, name="task-row"),
    path("<int:pk>/delete/", views.task_delete, name="task-delete"),
]
