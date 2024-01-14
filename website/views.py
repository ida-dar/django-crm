from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm
from .models import Record


def home(request):
  records = Record.objects.all()

  if request.method == "POST":
    username = request.POST.get('username')
    password = request.POST.get('password')
    user = authenticate(request, username=username, password=password)

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
