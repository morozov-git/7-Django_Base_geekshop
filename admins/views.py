from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.decorators import user_passes_test


from users.models import User
from .forms import UserAdminRegisterForm, UserAdminProfileForm


# Create your views here.
def index(request):
	return render(request, 'admins/admin.html')

@user_passes_test(lambda u: u.is_superuser)
def admin_users(request):
	context = {
		'users': User.objects.all()
	}
	return render(request, 'admins/admin-users-read.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_users_create(request):
	if request.method == 'POST':
		form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Пользователь успешно добавлен')
			return HttpResponseRedirect(reverse('admins:admin_users'))
	else:
		form = UserAdminRegisterForm()
	context = {
		'title': 'GeekShop-UserCreate',
		'form': form,
	}
	return render(request, 'admins/admin-users-create.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_users_update(request, id):
	users_select = User.objects.get(id=id)
	if request.method == 'POST':
		form = UserAdminProfileForm(data=request.POST, instance=users_select, files=request.FILES)
		if form.is_valid():
			form.save()
			messages.success(request, 'Профиль пользователя успешно изменен')
			return HttpResponseRedirect(reverse('admins:admin_users'))
	else:
		form = UserAdminProfileForm(instance=users_select)
	context = {
		'title': 'GeekShop - UserUpdate',
		'form': form,
		'users_select': users_select,
		}
	return render(request, 'admins/admin-users-update-delete.html', context)

@user_passes_test(lambda u: u.is_superuser)
def admin_users_delete(request, id):
	user = User.objects.get(id=id)
	user.delete()
	return HttpResponseRedirect(reverse('admins:admin_users'))

@user_passes_test(lambda u: u.is_superuser)
def admin_users_activation(request, id):
	user = User.objects.get(id=id)
	if user.is_active:
		user.is_active = False
		user.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
	else:
		user.is_active = True
		user.save()
		return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

