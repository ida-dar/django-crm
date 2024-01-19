from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.utils.safestring import SafeString

from .models import Record, Service, Product, Order


class SignupForm(UserCreationForm):
  email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                           required=True)
  first_name = forms.CharField(label="", max_length=50, min_length=1,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                               required=True)
  last_name = forms.CharField(label="", max_length=50, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                              required=True)

  class Meta:
    model = User
    fields = (
      'username',
      'first_name',
      'last_name',
      'email',
      'password1',
      'password2'
    )

  def __init__(self, *args, **kwargs):
    super(SignupForm, self).__init__(*args, **kwargs)

    self.fields['username'].widget.attrs['class'] = 'form-control'
    self.fields['username'].widget.attrs['placeholder'] = 'User Name'
    self.fields['username'].label = ''
    self.fields[
      'username'].help_text = '<span class="form-text text-muted"><small>Required. 150 characters or fewer. Letters, ' \
                              'digits and @/./+/-/_ only.</small></span>'

    self.fields['password1'].widget.attrs['class'] = 'form-control'
    self.fields['password1'].widget.attrs['placeholder'] = 'Password'
    self.fields['password1'].label = ''
    self.fields[
      'password1'].help_text = '<ul class="form-text text-muted small"><li>Your password can\'t be too similar to ' \
                               'your other personal information.</li><li>Your password must contain at least 8 ' \
                               'characters.</li><li>Your password can\'t be a commonly used password.</li><li>Your ' \
                               'password can\'t be entirely numeric.</li></ul>'

    self.fields['password2'].widget.attrs['class'] = 'form-control'
    self.fields['password2'].widget.attrs['placeholder'] = 'Confirm Password'
    self.fields['password2'].label = ''
    self.fields[
      'password2'].help_text = '<span class="form-text text-muted"><small>Enter the same password as before, ' \
                               'for verification.</small></span>'


class AddRecordForm(forms.ModelForm):
  first_name = forms.CharField(label="", max_length=50, min_length=1,
                               widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name'}),
                               required=True)
  last_name = forms.CharField(label="", max_length=50, min_length=1,
                              widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name'}),
                              required=True)
  email = forms.EmailField(label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}),
                           required=True)
  phone = forms.CharField(label="", max_length=15, min_length=1,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Phone'}),
                          required=True)
  address = forms.CharField(label="", max_length=100, min_length=1,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Address'}),
                            required=True)
  city = forms.CharField(label="", max_length=100, min_length=1,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'City'}),
                         required=True)
  state = forms.CharField(label="", max_length=50, min_length=1,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'State'}),
                          required=True)
  zipcode = forms.CharField(label="", max_length=15, min_length=1,
                            widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Zipcode'}),
                            required=True)

  def as_div(self):
    return SafeString(super().as_div().replace("<div>", "<div class='col-md-6 col-sm-12'>"))

  class Meta:
    model = Record
    exclude = ("user", "activated_services")


class AddServiceForm(forms.ModelForm):
  name = forms.CharField(label="", max_length=50, min_length=1,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                         required=True)
  price = forms.CharField(label="", max_length=50, min_length=1,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price ($)'}),
                          required=True)
  description = forms.CharField(label="", max_length=2000,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide service '
                                                                                                     'description',
                                                             'rows': '3'}),
                                required=True)

  def as_div(self):
    return SafeString(super().as_div().replace("<div>", "<div class='col-12'>"))

  class Meta:
    model = Service
    fields = (
      'name',
      'price',
      'description',
    )


class AddProductForm(forms.ModelForm):
  name = forms.CharField(label="", max_length=50, min_length=1,
                         widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'}),
                         required=True)
  price = forms.CharField(label="", max_length=50, min_length=1,
                          widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Price ($)'}),
                          required=True)
  amount = forms.CharField(label="", max_length=50, min_length=1,
                           widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Amount'}),
                           required=True)
  description = forms.CharField(label="", max_length=2000,
                                widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Provide service '
                                                                                                     'description',
                                                             'rows': '3'}),
                                required=True)

  def as_div(self):
    return SafeString(super().as_div().replace("<div>", "<div class='col-12'>"))

  class Meta:
    model = Product
    fields = (
      'name',
      'price',
      'amount',
      'description',
    )


class AddOrderForm(forms.ModelForm):
  client_name = forms.ModelChoiceField(queryset=Record.objects.all(),
                                       widget=forms.Select(attrs={'class': 'form-control'}),
                                       required=True,
                                       ),
  activated_services = forms.ModelChoiceField(queryset=Service.objects.all(),
                                              widget=forms.Select(attrs={'class': 'form-control'}),
                                              required=True,
                                              ),
  ordered_products = forms.ModelChoiceField(queryset=Product.objects.all(),
                                            widget=forms.Select(attrs={'class': 'form-control'}),
                                            required=True,
                                            ),

  def as_div(self):
    return SafeString(super().as_div().replace("<div>", "<div class='col-12'>"))

  def __init__(self, *args, **kwargs):
    super(AddOrderForm, self).__init__(*args, **kwargs)

    self.fields['client_name'].widget.attrs['class'] = 'form-select my-3'
    self.fields['client_name'].widget.attrs['placeholder'] = 'Client'
    self.fields['client_name'].label = ''

    self.fields['activated_services'].widget.attrs['class'] = 'form-select my-3'
    self.fields['activated_services'].widget.attrs['placeholder'] = 'Services'
    self.fields['activated_services'].label = ''

    self.fields['ordered_products'].widget.attrs['class'] = 'form-select my-3'
    self.fields['ordered_products'].widget.attrs['placeholder'] = 'Products'
    self.fields['ordered_products'].label = ''

  class Meta:
    model = Order
    fields = (
      'client_name',
      'activated_services',
      'ordered_products',
    )
