from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages


def home(request):
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
    return render(request, 'home.html', {})


def logout_user(request):
  logout(request)

  # if request.user.is_authenticated:
  #   messages.error(request, "There was an error logging out. Please try again", extra_tags='danger')
  #   return redirect('home')
  # else:
  messages.success(request, "Logged out successfully", extra_tags='success')
  return redirect('home')


def register_user(request):
  return render(request, 'register.html', {})
