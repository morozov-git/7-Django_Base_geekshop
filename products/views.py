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













def test(request):
	context = {
		"title": "geekshop_tast",
		"user": "UserName",
		"description": "Hello world!",
		# "test": test1(),
		"products": [
			{"name": "Худи черного цвета с монограммами adidas Originals 111", "price": 6091},
			{"name": "Худи черного цвета с монограммами adidas Originals 222", "price": 6092}
		],
		"promotion": True,
		# "discount": discount(product.price),
	}
	return render(request, "test.html", context)

# def discount(price):
# 	return price-(price/100)*25
# with open("templates/products.json", "r", encoding="ut8-8") as goods:
