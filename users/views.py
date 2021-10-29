from django.conf import settings
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import send_mail
from django.shortcuts import render, HttpResponseRedirect
from django.contrib import auth, messages
from django.urls import reverse, reverse_lazy
from users.models import User
from .forms import UserLoginForm, UserRegisterForm, UserProfileForm, UserProfileEditForm
from baskets.models import Basket
from django.contrib.auth.decorators import login_required


# Create your views here.

class LoginListView(LoginView):
    template_name = 'users/login.html'
    form_class = UserLoginForm
    success_url = 'index'

    def get(self, request, *args, **kwargs):
        sup = super(LoginListView, self).get(request, *args, **kwargs)
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy(self.success_url))
        return sup

    def get_context_data(self, **kwargs):
        context = super(LoginListView, self).get_context_data(**kwargs)
        context['title'] = 'GeekShop - Авторизация'
        return context



# def login(request):
# 	if request.method == 'POST':
# 		form = UserLoginForm(data=request.POST)
# 		if form.is_valid():
# 			username = request.POST['username']
# 			password = request.POST['password']
# 			user = auth.authenticate(username=username, password=password)
# 			if user and user.is_active:
# 				auth.login(request, user)
# 				test = form.errors
# 				return HttpResponseRedirect(reverse('index'))
# 	# else:
# 	# 	print(form.errors)
# 	# 	# return HttpResponseRedirect(reverse('users:login'))
# 	else:
# 		form = UserLoginForm()
# 	context = {
# 		'title': 'GeekShop - Авторизация',
# 		'form': form
# 	}
# 	return render(request, 'users/login.html', context)


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

	try:
		requestImageURL = request.user.image.url
		#нужно подменить ссылку на изобрыжение в профиле, если оно загружается со стороннего ресурса(содержит http://)
		requestImageName = request.user.image.name
		requestImageURL = request.user.image.url
		# formImageName = form['image'].initial.name #.imageName
		# formImageUrl = form['image'].initial.url #.imageURL
		# form_iamge = form['image']
		# Для сохранения ссылки пробовал изменять данные полученные из form и request
		profile_image = request.user.image.url
		if profile_image.find('/media/http') != -1:
			# Как правильно подменить данные в form или request чтобы не вводить
			# дополнительную переменную (profile_image) и не передавать ее в контекст?

			# при таком изменении данных выходила ошибка
			# request.user.image.url = requestImageName
			# form['image'].initial.url = formImageName
			profile_image = request.user.image.name
	except:
		profile_image = 0



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


