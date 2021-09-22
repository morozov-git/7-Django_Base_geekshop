"""geekshop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from admins.views import index, UserListView, UserCreteView, UserUpdateView, UserDeleteView, UserActivateView
from admins.views import ProductsListView, ProductUpdateView, ProductCreateView, ProductDeleteView
# admin_users, admin_users_create, admin_users_update, admin_users_delete, admin_users_activation


from django.conf import settings
from django.conf.urls.static import static

app_name = "admins"

urlpatterns = [
	path('', index, name='index'),
	path('users/', UserListView.as_view(), name='admin_users'),  # адрес для CBV
	path('user-create/', UserCreteView.as_view(), name='admin_users_create'),  # адрес для CBV
	path('user-update/<int:pk>', UserUpdateView.as_view(), name='admin_users_update'),  # адрес для CBV
	path('user-delete/<int:pk>', UserDeleteView.as_view(), name='admin_users_delete'),  # адрес для CBV
	path('user-activate/<int:pk>', UserActivateView.as_view(), name='admin_users_activation'),  # адрес для CBV
	path('products/', ProductsListView.as_view(), name='admin_products'),  # адрес для CBV
	path('product-create/', ProductCreateView.as_view(), name='admin_product_create'),
	path('product-update/<int:pk>', ProductUpdateView.as_view(), name='admin_product_update'),  # адрес для CBV
	path('product-delete/<int:pk>', ProductDeleteView.as_view(), name='admin_product_delete'),  # адрес для CBV
	# path('product-update/<int:pk>', ProductUpdateView.as_view(), name='admin_product_update'),
	# path('user-create/', admin_users_create, name='admin_users_create'), # адрес для FBV
	# path('user-update/<int:id>', admin_users_update, name='admin_users_update'),    # адрес для FBV
	# path('users/', admin_users, name='admin_users'),      # адрес для FBV
	# path('user-delete/<int:id>', admin_users_delete, name='admin_users_delete'),    # адрес для FBV
	# path('user-activate/<int:id>', admin_users_activation, name='admin_users_activation'),  # адрес для FBV
]
