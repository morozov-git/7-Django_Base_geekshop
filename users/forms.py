import hashlib
import random

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UserChangeForm

from django import forms

import users
from users.models import User


class UserProfileForm(UserChangeForm):
	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	email = forms.EmailField(widget=forms.EmailInput(attrs={'readonly': True}))
	username = forms.CharField(widget=forms.TextInput(attrs={'readonly': True}))
	age = forms.IntegerField(widget=forms.NumberInput(), required=False)
	image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-input'}), required=False)

	class Meta:
		model = User
		fields = ('username', 'email', 'age', 'first_name', 'last_name', 'image')

	def clean_image(self):
		if self.cleaned_data['image']:
			data = self.cleaned_data['image']
			if data.size > 1050000:
				raise forms.ValidationError("Слишком большой файл! Выберите файл меньше 1МБ.")
			return data


	def __init__(self, *args, **kwargs):
		super(UserProfileForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
		self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес электронной почты'
		self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
		self.fields['age'].widget.attrs['placeholder'] = 'Введите ваш возраст'
		for field_name, field in self.fields.items():
			if field_name != 'image':
				field.widget.attrs['class'] = 'form-control  py-4'


class UserLoginForm(AuthenticationForm):
	username = forms.CharField(widget=forms.TextInput())
	password = forms.CharField(widget=forms.PasswordInput())

	class Meta:
		model = User
		fields = ('password', 'username')

	def __init__(self, *args, **kwargs):
		super(UserLoginForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
		self.fields['password'].widget.attrs['placeholder'] = 'Введите пароль'
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control  py-4'


class UserRegisterForm(UserCreationForm):
	username = forms.CharField(widget=forms.TextInput())
	email = forms.EmailField(widget=forms.EmailInput())
	first_name = forms.CharField(widget=forms.TextInput())
	last_name = forms.CharField(widget=forms.TextInput())
	password1 = forms.CharField(widget=forms.PasswordInput())
	password2 = forms.CharField(widget=forms.PasswordInput())
	age = forms.IntegerField(widget=forms.NumberInput(), required=False)

	class Meta:
		model = User
		fields = ('username', 'email', 'first_name', 'last_name', 'age', 'password1', 'password2')

	def __init__(self, *args, **kwargs):
		super(UserRegisterForm, self).__init__(*args, **kwargs)
		self.fields['username'].widget.attrs['placeholder'] = 'Введите имя пользователя'
		self.fields['email'].widget.attrs['placeholder'] = 'Введите адрес электронной почты'
		self.fields['first_name'].widget.attrs['placeholder'] = 'Введите имя'
		self.fields['last_name'].widget.attrs['placeholder'] = 'Введите фамилию'
		self.fields['age'].widget.attrs['placeholder'] = 'Введите ваш возраст'
		self.fields['password1'].widget.attrs['placeholder'] = 'Введите пароль'
		self.fields['password2'].widget.attrs['placeholder'] = 'Подтвердите пароль'
		for field_name, field in self.fields.items():
			field.widget.attrs['class'] = 'form-control  py-4'

	def clean_email(self):
		if self.data['email']:
			email = self.cleaned_data['email']
			if User.objects.filter(email=email).exists():
				raise forms.ValidationError("Пользователь с таким адресом электронной почты уже существует.")
			return email

	def save(self, commit=True):
		user = super(UserRegisterForm, self).save()
		user.is_active = False
		salt = hashlib.sha1(str(random.random()).encode('utf8')).hexdigest()[:6]
		user.activation_key = hashlib.sha1((user.email + salt).encode('utf8')).hexdigest()
		user.save()
		return user
