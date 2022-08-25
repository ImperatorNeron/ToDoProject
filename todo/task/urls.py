from django.urls import path
from .views import *
from django.contrib.auth.views import LogoutView

# todo: check and rename https://betterprogramming.pub/10-best-practices-for-naming-rest-api-endpoints-442ae592a3a0
urlpatterns = [
    path('', Index.as_view(), name="main_page"),
    path('Tasks/', LookMyTasks.as_view(), name="task_page"),
    path('CreateTask/', CreateTask.as_view(), name="task_create"),
    path('DeleteTask/task-<int:pk>', DeleteTask.as_view(), name="task_delete"),
    path('UpdateTask/task-<int:pk>', UpdateTask.as_view(), name="edit_task"),
    path('Login/', LoginAccount.as_view(), name="login"),
    path('logout/', LogoutView.as_view(next_page="main_page"), name="logout"),
    path('registration/', RegisterAccount.as_view(), name="registration"),
    path('<slug:slug>/profile/', ProfileCheck.as_view(), name="check"),
    path('<slug:slug>/edit-profile/', ProfileEdit.as_view(), name="edit"),
    path('Rating/', Rating.as_view(), name="rating"),
    path('complete/task-<int:pk>', complete, name='complete'),
    path('<slug:slug>/check/', CheckSomebodyProfile.as_view(), name='check_somebody'),
    path('DeleteDoneTasks/', delete_all_completed_tasks, name='DeleteDoneTasks'),
]
