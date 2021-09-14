from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.models import User
from .forms import UserLoginForm, UserRegisterForm


# Create your views here.

def login(request):
	if request.method == 'POST':
		form = UserLoginForm(data=request.POST)
		if form.is_valid():
			username = request.POST['username']
			password = request.POST['password']
			user = auth.authenticate(username=username, password=password)
			if user and user.is_active:
				auth.login(request, user)
				test = form.errors
				return HttpResponseRedirect(reverse('index'))
		# else:
		# 	print(form.errors)
		# 	# return HttpResponseRedirect(reverse('users:login'))
	else:
		form = UserLoginForm()
	context = {
		'title': 'GeekShop - Авторизация',
		'form': form
	}

	return render(request, 'users/login.html', context)


def register(request):
	form = UserRegisterForm()
	if request.method == 'POST':
		form = UserRegisterForm(data=request.POST)
		if form.is_valid():
			form.save()
			messages.success(request, 'Вы успешно зарегистрировались')
			return HttpResponseRedirect(reverse('users:login'))
		# else:
		# 	print(form.errors)
		# 	return HttpResponseRedirect(reverse('users:register'))
		# else:
			#form = UserRegisterForm()
	context = {
		'title': 'GeekShop - Регистрация',
		'form': form
	}
	return render(request, 'users/register.html', context)


def logout(request):
	auth.logout(request)
	return HttpResponseRedirect(reverse('index'))


def edit(request):
	return HttpResponseRedirect(reverse('index'))
