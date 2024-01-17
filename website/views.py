import os
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record


def home(request):
  records = Record.objects.all()

  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    remember_me = request.POST.get('remember_me')

    user = authenticate(request, username=username, password=password)

    if remember_me is None:
      # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
      request.session.set_expiry(0)
      # Set session as modified to force data updates/cookie to be saved.
      request.session.modified = True

    if user is not None:
      login(request, user)
      messages.success(request, "Logged in successfully", extra_tags='success')
      return redirect('home')
    else:
      messages.error(request, "There was an error logging in. Please try again", extra_tags='danger')
      return redirect('home')
  else:
    return render(request, 'home.html', {'records': records})


def logout_user(request):
  logout(request)

  if request.user.is_authenticated:
    messages.error(request, "There was an error logging out. Please try again", extra_tags='danger')
    return redirect('home')
  else:
    messages.success(request, "Logged out successfully", extra_tags='success')
    return redirect('home')


def register_user(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      form.save()
      username = form.cleaned_data['username']
      password = form.cleaned_data['password1']
      user = authenticate(username=username, password=password)
      login(request, user)
      if request.user.is_authenticated:
        messages.success(request, "Registration was successful", extra_tags='success')
        return redirect('home')
      else:
        messages.error(request, "There was an error. Please try again", extra_tags='danger')
        return redirect('home')
  else:
    form = SignupForm()
    return render(request, 'register.html', {'form': form})

  return render(request, 'register.html', {'form': form})


def customer_record(request, pk):
  if request.user.is_authenticated:
    record = Record.objects.get(id=pk)
    return render(request, 'customer_record.html', {'record': record})

  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return redirect('home')


def notify_record(request, pk):
  record = Record.objects.filter(pk=pk).values()
  record_email = record[0]['email']

  if request.method == 'POST':
    subject = request.POST.get('subject')
    message = request.POST.get('message')

    if record_email and subject and message:

      send_mail(
        subject=subject,
        message=message,
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[record_email, ],
      )
      messages.success(request, "Email sent successfully", extra_tags='success')
      return redirect('home')
    else:
      messages.error(request, "There was an error while sending email. Please try again.", extra_tags='danger')
  else:
    return render(request, 'notify_record.html', {'record_email': record_email})


def add_record(request):
  form = AddRecordForm(request.POST or None)
  if request.user.is_authenticated:
    if request.method == 'POST' and form.is_valid():
      add_record = form.save()
      messages.success(request, "Record added successful", extra_tags='success')
      return redirect('home')
    else:
      return render(request, 'add_record.html', {'form': form})
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return redirect('home')


def update_record(request, pk):
  if request.user.is_authenticated:
    curr_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=curr_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Record updated successful", extra_tags='success')
      return redirect('home')
    return render(request, 'update_record.html', {'form': form})
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return redirect('home')


def delete_record(request, pk):
  if request.user.is_authenticated:
    record = Record.objects.get(id=pk)
    record.delete()

    if record is None:
      messages.error(request, f"There was an error while deleting record with id: {pk}. Please try again",
                     extra_tags='danger')
    else:
      messages.success(request, "Record deleted successfully", extra_tags='success')
      return redirect('home')
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return redirect('home')
