from django.urls import path
from django.contrib.auth.views import LogoutView

from task.views import CustomLoginView, RegisterForm
from task.views import TaskList, TaskCreate, TaskUpdate, TaskDelete


urlpatterns = [
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
    path('register/', RegisterForm.as_view(), name='register'),
    path('', TaskList.as_view(), name='home'),
    path('update-task/<str:pk>/', TaskUpdate.as_view(), name='updatetask'),
    path('delete-task/<str:pk>/', TaskDelete.as_view(), name='deletetask'),
    path('new-task/', TaskCreate.as_view(), name='newtask'),
]
