from django.shortcuts import render
import json

with open("static/products.json", "r", encoding="utf-8") as goods:
	products_list = json.load(goods)


# Create your views here.
def index(request):
	context = {"title": "geek shop"}
	return render(request, "index.html", context)


def products(request):
	context = {
		"title": "geek shop catalog",
		"products_list": products_list
	}
	return render(request, "products.html", context)













