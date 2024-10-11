from django.contrib import admin
from django.urls import path, include

from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('', views.login_view, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'),
    path('violation/', views.violation_form, name='violation_form'),  # For new violation
    path('violation/<int:id>/', views.violation_form, name='violation_edit'),  # For editing an existing violation
    path('violations/', views.violation_list, name='violation_list'),  # To view the list of violations
    # Add other paths here if needed
]