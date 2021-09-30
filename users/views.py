from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse
from users.models import User
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
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
				messages.success(request, 'Для завершения регистрации перейдите по ссылке в письме') #(request, 'Вы успешно зарегистрировались')
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
		profile_form = UserProfileEditForm(data=request.POST, instance=request.user.userprofile)
		if form.is_valid() and profile_form.is_valid():
			form.save()
			messages.success(request, 'Профиль успешно изменен')
			return HttpResponseRedirect(reverse('users:profile'))
	else:
		profile_form = UserProfileEditForm(instance=request.user.userprofile)
		form = UserProfileForm(instance=request.user)

		#нужно подменить ссылку на изобрыжение в профиле, если оно загружается со стороннего ресурса(содержит http://)
		requestImageName = request.user.image.name
		requestImageURL = request.user.image.url
		# formImageName = form['image'].initial.name #.imageName
		# formImageUrl = form['image'].initial.url #.imageURL
		# form_iamge = form['image']
		profile_image = request.user.image.url
		if profile_image.find('/media/http') != -1:
			profile_image = request.user.image.name


	context = {
		'title': 'GeekShop - Профиль',
		'form': form,
		'profile_form': profile_form,
		'profile_image': profile_image
		# 'baskets': Basket.objects.filter(user=request.user), # после подключения контекстного процессора можно отключить
	}
	return render(request, 'users/profile.html', context)


def send_verify_link(user):
	verify_link = reverse('users:verify', args=[user.email, user.activation_key])
	subject = f'Для активации учетной записи {user.username} перейдите по ссылке'
	message = f'Для подтверждения учетной записи {user.username} на портале {settings.DOMAIN_NAME} \n' \
			  f'перейдите по ссылке: {settings.DOMAIN_NAME}{verify_link}'
	return send_mail(subject, message, settings.EMAIL_HOST_USER, [user.email], fail_silently=False)


def verify(request, email, activation_key):
	try:
		user = User.objects.get(email=email)
		if user and user.activation_key == activation_key and not user.is_activation_key_expired():
			user.activation_key = ''
			user.activation_key_expires = None
			user.is_active = True
			user.save()
			auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')
		return render(request, 'users/verification.html')
	except Exception as e:
		print(f'error activation user : {e.args}')
		return HttpResponseRedirect(reverse('index'))


