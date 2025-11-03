from django.urls import path
from .views import hello
from .views import generate_mockup_view,get_task_status,MockupListView

urlpatterns = [
    path('hello/', hello),
    path('mockups/generate/', generate_mockup_view),
    path('tasks/<str:task_id>/', get_task_status),
    path('mockups/', MockupListView.as_view()), 
]