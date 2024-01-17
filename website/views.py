from django.http import HttpResponseRedirect
from django.dispatch import receiver
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render
from django.db.models.signals import pre_save
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignupForm, AddRecordForm
from .models import Record
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

UserModel = get_user_model()


def home(request):
  records = Record.objects.all()
  all_users = UserModel.objects.values()

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
    else:
      messages.error(request, "There was an error logging in. Please try again", extra_tags='danger')

    return HttpResponseRedirect('')
  else:
    return render(request, 'home.html', {'records': records, 'all_users': all_users})


def logout_user(request):
  logout(request)

  if request.user.is_authenticated:
    messages.error(request, "There was an error logging out. Please try again", extra_tags='danger')
    return HttpResponseRedirect('')
  else:
    messages.success(request, "Logged out successfully", extra_tags='success')
    return HttpResponseRedirect('')


@receiver(pre_save, sender=User)
def set_new_user_inactive(sender, instance, **kwargs):
  if instance._state.adding is True:
    print("Creating Inactive User")
    instance.is_active = False
  else:
    print("Updating User Record")


def register_user(request):
  if request.method == 'POST':
    form = SignupForm(request.POST)
    if form.is_valid():
      user = form.save()

      if user is not None:
        login(request, user)
      if request.user.is_authenticated:
        messages.success(request, "Registration was successful", extra_tags='success')
        return HttpResponseRedirect('')
      else:
        messages.error(request, "There was an error. Please try again", extra_tags='danger')
        return HttpResponseRedirect('')
  else:
    form = SignupForm()
    return render(request, 'register.html', {'form': form})

  return render(request, 'register.html', {'form': form})


def approve_user(request, pk):
  user = User.objects.get(pk=pk)
  user.is_active = True
  user.save()

  if user.is_active:
    messages.success(request, "User activated successfully", extra_tags='success')
  else:
    messages.error(request, "There was an error. Please try again", extra_tags='danger')

  return HttpResponseRedirect('')


def customer_record(request, pk):
  if request.user.is_authenticated:
    record = Record.objects.get(id=pk)
    return render(request, 'customer_record.html', {'record': record})

  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return HttpResponseRedirect('')


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
      return HttpResponseRedirect('')
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
      return HttpResponseRedirect('')
    else:
      return render(request, 'add_record.html', {'form': form})
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return HttpResponseRedirect('')


def update_record(request, pk):
  if request.user.is_authenticated:
    curr_record = Record.objects.get(id=pk)
    form = AddRecordForm(request.POST or None, instance=curr_record)
    if form.is_valid():
      form.save()
      messages.success(request, "Record updated successful", extra_tags='success')
      return HttpResponseRedirect('')
    return render(request, 'update_record.html', {'form': form})
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return HttpResponseRedirect('')


def delete_record(request, pk):
  if request.user.is_authenticated:
    record = Record.objects.get(id=pk)
    record.delete()

    if record is None:
      messages.error(request, f"There was an error while deleting record with id: {pk}. Please try again",
                     extra_tags='danger')
    else:
      messages.success(request, "Record deleted successfully", extra_tags='success')
      return HttpResponseRedirect('')
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return HttpResponseRedirect('')
