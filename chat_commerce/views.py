from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse

from .models import Request, Offer


class RequestListView(ListView):
    model = Request
    template_name = 'chat_commerce/request_list.html'
    raise_exception = True

class OfferListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'chat_commerce/offer_list.html'
    raise_exception = True

    def get_queryset(self):
        return Offer.objects.filter(User=self.request.user)

def make_offer(Request):
    print(f'hola {Request.User.username}')
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    fields = ['category', 'name', 'desc', 'image', 'price']
    template_name = 'store/products/create.html'
    
    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.slug = slugify(form.instance.name)
        form.save()
        return redirect(reverse_lazy('store:product_list'))