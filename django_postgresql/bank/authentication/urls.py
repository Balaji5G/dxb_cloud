from django.urls import path
from . import views

urlpatterns = [
    path('token/', views.LoginView.as_view(), name="")
]
