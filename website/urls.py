from django.urls import path
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('logout/', views.logout_user, name='logout'),
  path('register/', views.register_user, name='register'),
  path('record/<int:pk>', views.customer_record, name='record'),  # pass primary key
]
