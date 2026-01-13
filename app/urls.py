from django.urls import path
from . import views

urlpatterns = [
    path('email-tool/', views.email_tool_view, name='email_tool'),
    path('progress/<task_id>/', views.get_progress, name='progress'),
]
