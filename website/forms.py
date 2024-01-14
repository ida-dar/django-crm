from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .models import Record


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

  class Meta:
    model = Record
    exclude = ("user",)
