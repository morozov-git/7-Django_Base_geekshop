from django.shortcuts import render

# Create your views here.
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView

class OrderList(ListView):
	pass

class OrderCreate(CreateView):
	pass

class OrderUpdate(UpdateView):
	pass

class OrderDelete(DeleteView):
	pass

class OrderRead(DetailView):
	pass

class OrderItemsCreate(CreateView):
	pass

class order_forming_comlete(request, pk):
	pass




