from django.urls import path
from . import views

urlpatterns = [
    path('', views.welcome, name='welcome'),  # Welcome page
    path('dashboard/', views.dashboard, name='dashboard'),  # Dashboard page
    path('healthz', views.healthz, name='healthz')  #healthcheck endpoint
]