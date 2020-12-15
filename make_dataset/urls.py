from django.urls import path
from . import views

urlpatterns = [
    path('update_admin_only/', views.update_dataset),
]
