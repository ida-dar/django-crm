from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
  path('', views.home, name='home'),
  path('logout/', views.logout_user, name='logout'),
  path('register/', views.register_user, name='register'),
  path('approve_user/<int:pk>', views.approve_user, name='approve_user'),

  path('record/<int:pk>', views.customer_record, name='record'),  # pass primary key
  path('add_record', views.add_record, name='add_record'),
  path('update_record/<int:pk>', views.update_record, name='update_record'),
  path('delete_record/<int:pk>', views.delete_record, name='delete_record'),

  path('notify_record/<int:pk>', views.notify_record, name='notify_record'),

  path('reset_password/', auth_views.PasswordResetView.as_view(template_name='reset_password.html'),
       name='reset_password'),
  path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name='reset_password_sent.html'),
       name='password_reset_done'),
  path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name='reset_password_form.html'),
       name='password_reset_confirm'),
  path('reset_password_complete/',
       auth_views.PasswordResetCompleteView.as_view(template_name='reset_password_complete.html'),
       name='password_reset_complete'),
]
