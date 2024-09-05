from django.urls import path
from . import views

urlpatterns = [
    path('auth/register/', views.register, name='register'),
    path('auth/login/', views.login, name='login'),
    path('user/update/<int:key>/', views.update_user, name='update_user'),
    path('user/delete/<int:key>/', views.delete_user, name='delete_user'),
]
