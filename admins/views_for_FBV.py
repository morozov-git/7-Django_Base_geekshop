from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from .forms import UserAdminRegisterForm, UserAdminProfileForm


# Create your views here.
@user_passes_test(lambda u: u.is_superuser)
def index(request):
	return render(request, 'admins/admin.html')


class UserListView(ListView):
	model = User
	# context_object_name = 'users'  # Если хотим использовать в шаблонах вместо object_list
	template_name = 'admins/admin-users-read.html'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(UserListView, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop-Users'
		return context

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(UserListView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users(request):
# 	context = {
# 		'users': User.objects.all()
# 	}
# 	return render(request, 'admins/admin-users-read.html', context)


class UserCreteView(CreateView):
	model = User
	template_name = 'admins/admin-users-create.html'
	form_class = UserAdminRegisterForm
	success_url = reverse_lazy('admins:admin_users')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(UserCreteView, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop-UserCreate'
		return context

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(UserCreteView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_create(request):
# 	if request.method == 'POST':
# 		form = UserAdminRegisterForm(data=request.POST, files=request.FILES)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, 'Пользователь успешно добавлен')
# 			return HttpResponseRedirect(reverse('admins:admin_users'))
# 	else:
# 		form = UserAdminRegisterForm()
# 	context = {
# 		'title': 'GeekShop-UserCreate',
# 		'form': form,
# 	}
# 	return render(request, 'admins/admin-users-create.html', context)

class UserUpdateView(UpdateView, id):
	model = User
	template_name = 'admins/admin-users-update-delete.html'
	form_class = UserAdminProfileForm
	success_url = reverse_lazy('admins:admin_users')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(UserUpdateView, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop - UserUpdate'
		return context

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(UserUpdateView, self).dispatch(request, *args, **kwargs)


# @user_passes_test(lambda u: u.is_superuser)
# def admin_users_update(request, id):
# 	users_select = User.objects.get(id=id)
# 	if request.method == 'POST':
# 		form = UserAdminProfileForm(data=request.POST, instance=users_select, files=request.FILES)
# 		if form.is_valid():
# 			form.save()
# 			messages.success(request, 'Профиль пользователя успешно изменен')
# 			return HttpResponseRedirect(reverse('admins:admin_users'))
# 	else:
# 		form = UserAdminProfileForm(instance=users_select)
# 	context = {
# 		'title': 'GeekShop - UserUpdate',
# 		'form': form,
# 		'users_select': users_select,
# 	}
# 	return render(request, 'admins/admin-users-update-delete.html', context)


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
