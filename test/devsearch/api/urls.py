from django.urls import path

from projects import views
from .  import views

urlpatterns = [
    path('', views.getRoutes),
    path('projects/', views.getProjects),  
    path('projects/<str:pk>/', views.getProject),  
  
]
