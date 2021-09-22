from django.contrib import messages
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse, reverse_lazy
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView

from users.models import User
from products.models import Product, ProductsCategory
from .forms import UserAdminRegisterForm, UserAdminProfileForm, ProductEditForm, CategoryEditForm


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


class UserUpdateView(UpdateView):
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


class UserDeleteView(DeleteView):
	model = User
	template_name = 'admins/admin-users-update-delete.html'
	success_url = reverse_lazy('admins:admin_users')

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(UserDeleteView, self).dispatch(request, *args, **kwargs)


class UserActivateView(UserDeleteView):
	def delete(self, request, *args, **kwargs):
		self.object = self.get_object()
		if self.object.is_active:
			self.object.is_active = False
			self.object.save()
		else:
			self.object.is_active = True
			self.object.save()
		return HttpResponseRedirect(self.get_success_url())

class ProductsListView(ListView):
	model = Product
	template_name = 'admins/admin-products-read.html'

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductsListView, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop-Products'
		return context

class ProductUpdateView(UpdateView):
	model = Product
	template_name = 'admins/admin-products-update-delete.html'
	form_class = ProductEditForm
	success_url = reverse_lazy('admins:admin_products')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductUpdateView, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop - ProductUpdate'
		return context

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductUpdateView, self).dispatch(request, *args, **kwargs)

class ProductCreateView(CreateView):
	model = Product
	template_name = 'admins/admin-products-create.html'
	form_class = ProductEditForm
	success_url = reverse_lazy('admins:admin_products')

	def get_context_data(self, *, object_list=None, **kwargs):
		context = super(ProductCreateView, self).get_context_data(**kwargs)
		context['title'] = 'GeekShop - ProductCreate'
		return context

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductCreateView, self).dispatch(request, *args, **kwargs)

class ProductDeleteView(DeleteView):
	model = Product
	template_name = 'admins/admin-products-update-delete.html'
	success_url = reverse_lazy('admins:admin_products')

	@method_decorator(user_passes_test(lambda u: u.is_superuser))
	def dispatch(self, request, *args, **kwargs):
		return super(ProductDeleteView, self).dispatch(request, *args, **kwargs)