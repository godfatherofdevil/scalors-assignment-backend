from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views

urlpatterns = [
    path('api/v1/board', views.BoardList.as_view(), name='boardList'),
    path('api/v1/board/<int:pk>', views.BoardDetail.as_view(), name='boardDetail'),
    path('api/v1/board/<int:pk>/todo', views.TodoList.as_view(), name='todoList'),
    path('api/v1/board/<int:pk>/todo/<int:id>', views.TodoDetail.as_view(), name='todoDetail'),
    path('api/v1/users', views.UserList.as_view(), name='userList'),
    path('api/v1/users/<int:pk>', views.UserDetail.as_view(), name='userDetail'),
    path('api/v1/reminders', views.ReminderList.as_view(), name='reminderList'),
    path('api/v1/reminders/<int:pk>', views.ReminderDetail.as_view(), name='reminderDetail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
