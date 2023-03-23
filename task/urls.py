from django.urls import path

from task import views

urlpatterns = [
    path('', views.list_tasks, name='list'),
    path('add', views.add_task, name='add'),
    path('mark_as_completed', views.mark_as_completed, name='mark_as_completed'),
    path('<int:task_id>/modify', views.modify_task, name='modify'),
    path('<int:task_id>/delete', views.delete_task, name='delete'),
]