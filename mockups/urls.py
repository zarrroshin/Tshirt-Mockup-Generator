from django.urls import path
from .views import hello
from .views import generate_mockup_view,task_status_view,MockupListView

urlpatterns = [
    path('hello/', hello),
    path('mockups/generate/', generate_mockup_view),
    path('tasks/<str:task_id>/',task_status_view ),
    path('mockups/', MockupListView.as_view()), 
]