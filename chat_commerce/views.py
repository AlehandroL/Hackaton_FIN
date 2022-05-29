from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Request, Offer


class RequestListView(ListView):
    model = Request
    template_name = 'chat_commerce/request_list.html'
    raise_exception = True

class OfferListView(ListView):
    model = Offer
    template_name = 'chat_commerce/offer_list.html'
    raise_exception = True