from collections import OrderedDict
from datetime import datetime
from urllib.parse import urlunparse, urlencode

import requests
from django.utils import timezone
from social_core.exceptions import AuthForbidden
from users.models import UserProfile


def save_user_profile(backend, user, response, *args, **kwargs):
	if backend.name != 'vk-oauth2':
		return
	api_url = urlunparse((
		'http',
		'api.vk.com',
		'/method/users.get',
		None,
		urlencode(OrderedDict(fields=','.join(('bdate', 'sex', 'about', 'domain', 'has_photo', 'personal', 'photo_100')),
							  access_token=response['access_token'],
							  v='5.131')),
		None
	))
	resp = requests.get(api_url)
	if resp.status_code != 200:
		return

	data = resp.json()['response'][0]

	if data['sex']:
		user.userprofile.gender = UserProfile.MALE if data['sex'] == 2 else UserProfile.FEMALE

	# if data['about']:
	# user_test_about = data['about']
	user_about = f"{data['about']}\n"
	user.userprofile.about_me = user_about
	# if data['personal']:
	# 	# lang = str(*data['personal']['langs'])
	# 	user_personal = f"Ссылка в VK: http://vk.com/{data['domain']}\n"
	# 	# user_personal = f"Язык: {lang}\n" \
	# 	# 				f"Ссылка в VK: http://vk.com/{data['domain']}\n"
	# 	user.userprofile.about_me = user_personal + user_about

	if data['has_photo'] == 1:
		user.image = data['photo_100']
		# Для сохранения фото пользователя в /media/
		# photo_link = data['photo_100']
		# photo_response = requests.get(photo_link)
		# path_photo = f'user_image/{user.pk}.jpg'
		# with open(f'media/{path_photo}', 'wb') as photo:
		# 	photo.write(photo_response.content)
		# user.image = path_photo
		# user.save()

	# try: # Пробуем получить возраст из профиля VK, если его нет в ответе сервера, то заполняем дату поумолчанию
	# 	bdate = datetime.strptime(data['bdate'],'%d.%m.%Y').date()
	# 	age = timezone.now().date().year - bdate.year
	# 	user.age = age
	# 	# return user.age
	# 	if age < 18:
	# 		user.delete()
	# 		raise AuthForbidden('social_core.backends.vk.VKOAuth2')
	# 	user.save()
	# 	return user
	# except:
	# 	user.save()
	user.save()

