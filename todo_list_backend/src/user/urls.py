from django.urls import path

from user import views

urlpatterns: list[path] = [
    path('user/', views.CreateUserAPIView.as_view()),
]
