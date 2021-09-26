from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.models import User
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm
from baskets.models import Basket
from django.contrib.auth.decorators import login_required


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
			user = form.save()
			if send_verify_link(user):
				messages.success(request, 'Вы успешно зарегистрировались')
			return HttpResponseRedirect(reverse('users:login'))
	# else:
	# 	print(form.errors)
	# 	return HttpResponseRedirect(reverse('users:register'))
	# else:
	# form = UserRegisterForm()
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


@login_required
def profile(request):
	if request.method == 'POST':
		form = UserProfileForm(data=request.POST, instance=request.user, files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Профиль успешно изменен')
			return HttpResponseRedirect(reverse('users:profile'))
	else:
		form = UserProfileForm(instance=request.user)
	context = {
		'title': 'GeekShop - Профиль',
		'form': form,
		'baskets': Basket.objects.filter(user=request.user),
	}
	return render(request, 'users/profile.html', context)


def send_verify_link(user):
	verify_link = reverse('users:verify', args=[user.email, user.activation_key])
	subject = f'Для активации учетной записи {user.username} перейдите по ссылке'
	message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} \n' \
			  f'перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
	return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
	# def verify(request, email, activation_key):
	pass
