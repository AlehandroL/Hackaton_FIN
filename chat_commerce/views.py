from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy

from .models import Request, Offer


class RequestListView(ListView):
    model = Request
    template_name = 'chat_commerce/request_list.html'
    raise_exception = True

class OfferedToYou_ListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'chat_commerce/offered_to_you_list.html'
    raise_exception = True

    def get_queryset(self):
        request_ids = Request.objects.filter(User=self.request.user).values_list('pk', flat=True)
        print(request_ids)
        return Offer.objects.filter(Request_id__in=request_ids)

class YourOffers_ListView(LoginRequiredMixin, ListView):
    model = Offer
    template_name = 'chat_commerce/your_offers.html'
    raise_exception = True

    def get_queryset(self):
        return Offer.objects.filter(User=self.request.user)



class OfferCreateView(LoginRequiredMixin, CreateView):
    model = Offer
    fields = ['date', 'start_time', 'end_time', 'message']
    template_name = 'chat_commerce/offer_create.html'
    
    def form_valid(self, form):
        form.instance.User = self.request.user
        form.instance.Request = Request.objects.get(pk=self.kwargs['id'])
        form.instance.active = True
        form.save()
        return redirect(reverse_lazy('chat_commerce:request_list'))