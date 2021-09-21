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
from admins.views import index, UserListView, admin_users_create, admin_users_update, admin_users_delete, admin_users_activation
#admin_users,


from django.conf import settings
from django.conf.urls.static import static

app_name = "admins"



urlpatterns = [
    path('', index, name='index'),
    # path('users/', admin_users, name='admin_users'),      # адрес для FBV
    path('users/', UserListView.as_view(), name='admin_users'),     # адрес для CBV
    path('user-create/', admin_users_create, name='admin_users_create'),
    path('user-update/<int:id>', admin_users_update, name='admin_users_update'),
    path('user-delete/<int:id>', admin_users_delete, name='admin_users_delete'),
    path('user-activate/<int:id>', admin_users_activation, name='admin_users_activation'),
]

