from django.urls import path

from task import views


urlpatterns: list[path] = [
    path('category/<str:category_id>/', views.CategoryAPIView.as_view()),
    path('categories/', views.CategoryAllAPIView.as_view()),
    path('task/<str:task_id>/', views.TaskAPIView.as_view()),
    path('tasks/', views.TaskAllAPIView.as_view()),
    path('tasks/<str:category_id>/', views.TaskAllByCategoryAPIView.as_view()),
]
