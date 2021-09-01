from django.shortcuts import render


# Create your views here.
def index(request):
	context = {
		"title": "GeekShop",
	}
	return render(request, "index.html", context)


def products(request):
	context = {
		"title": "GeekShop_Catalog",
	}
	return render(request, "products.html", context)













def test(request):
	context = {
		"title": "geekshop_tast",
		"user": "UserName",
		"description": "Hello world!",
		# "test": test1(),
		"prodicts": [
			{"name": "Худи черного цвета с монограммами adidas Originals 111", "price": 6091},
			{"name": "Худи черного цвета с монограммами adidas Originals 222", "price": 6092}
		],
		"promotion": True,
		# "discount": discount(product.price),
	}
	return render(request, "test.html", context)


# def discount(price):
# 	return price-(price/100)*25