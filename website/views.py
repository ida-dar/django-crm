from django.conf import settings
from django.dispatch import receiver
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models.signals import pre_save
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import SignupForm, AddRecordForm, AddServiceForm, AddProductForm, AddOrderForm
from .models import Record, Product, Service, Order

UserModel = get_user_model()


def home(request):
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

    return redirect('home')
  else:
    return render(request, 'home.html', {'all_users': all_users})


def clients(request):
  all_client = Record.objects.all()

  if request.user.is_authenticated:
    return render(request, 'clients.html', {'clients': all_client})
  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return redirect('home')


def services(request):
  all_services = Service.objects.all()

  if request.user.is_authenticated:
    return render(request, 'services.html', {'services': all_services})
  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return redirect('home')


def products(request):
  all_products = Product.objects.all()

  if request.user.is_authenticated:
    return render(request, 'products.html', {'products': all_products})
  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return redirect('home')


def orders(request):
  all_orders = Order.objects.all()

  if request.user.is_authenticated:
    return render(request, 'orders.html', {'orders': all_orders})
  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return redirect('home')


def logout_user(request):
  logout(request)

  if request.user.is_authenticated:
    messages.error(request, "There was an error logging out. Please try again", extra_tags='danger')
  else:
    messages.success(request, "Logged out successfully", extra_tags='success')
  return redirect('home')


def delete_user(request, pk):
  user = UserModel.objects.get(pk=pk)
  deleted = user.delete()

  if deleted:
    messages.success(request, "User activated successfully", extra_tags='success')
  else:
    messages.error(request, "There was an error. Please try again", extra_tags='danger')

  return redirect('home')


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
        messages.success(request, "Registration was successful. Please wait for the admin approval before signing in.",
                         extra_tags='success')
      else:
        messages.error(request, "There was an error. Please try again", extra_tags='danger')
      return redirect('home')
  else:
    form = SignupForm()
    return render(request, 'register.html', {'form': form})


@login_required
def approve_user(request, pk):
  user = User.objects.get(pk=pk)
  user.is_active = True
  user.save()

  if user.is_active:
    send_mail(
      subject='Registration approved',
      message='You have been approved by administrator. You may login to Django CRM.',
      from_email=settings.EMAIL_HOST_USER,
      recipient_list=[user.email, ],
    )
    messages.success(request, "User activated successfully", extra_tags='success')
  else:
    messages.error(request, "There was an error. Please try again", extra_tags='danger')
  return redirect('home')


def customer_record(request, pk):
  if request.user.is_authenticated:
    record = Record.objects.get(id=pk)
    return render(request, 'customer_record.html', {'record': record})

  else:
    messages.error(request, "You must be logged in to view this page", extra_tags='danger')
    return redirect('home')


def order_for_client(request):
  if request.method == 'POST':
    form = AddOrderForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, "Record added successful", extra_tags='success')
    else:
      messages.error(request, "There was an error. Please try again", extra_tags='danger')
    return redirect('clients')

  else:
    form = AddOrderForm()
    return render(request, 'make_order_for_client.html', {'form': form})


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
    else:
      messages.error(request, "There was an error while sending email. Please try again.", extra_tags='danger')
    return redirect('home')
  else:
    return render(request, 'notify_record.html', {'record_email': record_email})


@login_required
def add_record(request, view_name):
  form = ''
  if view_name == 'client':
    form = AddRecordForm(request.POST or None)
  elif view_name == 'service':
    form = AddServiceForm(request.POST or None)
  elif view_name == 'product':
    form = AddProductForm(request.POST or None)

  if request.user.is_authenticated:
    if request.method == 'POST' and form.is_valid():
      form.save()
      messages.success(request, "Record added successful", extra_tags='success')
      return redirect(f'{view_name}s')
    else:
      return render(request, 'add_record.html', {'form': form, 'view_name': view_name})
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return redirect('home')


@login_required
def update_record(request, view_name, pk):
  form = ''

  if request.user.is_authenticated:
    if view_name == 'client':
      curr_record = Record.objects.get(id=pk)
      form = AddRecordForm(request.POST or None, instance=curr_record)
    elif view_name == 'service':
      curr_record = Service.objects.get(id=pk)
      form = AddServiceForm(request.POST or None, instance=curr_record)
    elif view_name == 'product':
      curr_record = Product.objects.get(id=pk)
      form = AddProductForm(request.POST or None, instance=curr_record)

    if form.is_valid():
      form.save()
      messages.success(request, "Record updated successful", extra_tags='success')
      return redirect(f'{view_name}s')
    return render(request, 'update_record.html', {'form': form, 'view_name': view_name})
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return redirect('home')


@login_required
def delete_record(request, view_name, pk):
  model_mapping = {
    'client': Record,
    'service': Service,
    'product': Product,
  }

  model = model_mapping.get(view_name)

  if model:
    del_record = get_object_or_404(model, id=pk)
    del_record.delete()

    if del_record is None:
      messages.error(request, f"There was an error while deleting record with id: {pk}. Please try again",
                     extra_tags='danger')
    else:
      messages.success(request, "Record deleted successfully", extra_tags='success')
    return redirect(f'{view_name}s')
  else:
    messages.error(request, "You must be logged to perform this action", extra_tags='danger')
    return redirect('home')
