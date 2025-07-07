from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('camera/<int:pk>/', views.camera_detail, name='camera_detail'),
]