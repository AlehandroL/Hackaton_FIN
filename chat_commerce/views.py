from django.shortcuts import redirect
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django import forms
from django.contrib import messages


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

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(OfferCreateView, self).get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'})
        form.fields['start_time'].widget = forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        form.fields['end_time'].widget = forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        form.fields['message'].widget = forms.TextInput(attrs={'placeholder': 'Enter a message'})
        return form
    
    def form_valid(self, form):
        form.instance.User = self.request.user
        form.instance.Request = Request.objects.get(pk=self.kwargs['id'])
        form.instance.active = True
        form.save()
        messages.success(self.request, 'Your offer has been sent successfully!')
        return redirect(reverse_lazy('chat_commerce:your_offers'))


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = Request
    fields = ['date', 'start_time', 'end_time', 'message']
    template_name = 'chat_commerce/request_create.html'

    def get_form(self, form_class=None):
        if form_class is None:
            form_class = self.get_form_class()

        form = super(RequestCreateView, self).get_form(form_class)
        form.fields['date'].widget = forms.TextInput(attrs={'placeholder': 'YYYY-MM-DD'})
        form.fields['start_time'].widget = forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        form.fields['end_time'].widget = forms.TextInput(attrs={'placeholder': 'HH:MM:SS'})
        form.fields['message'].widget = forms.TextInput(attrs={'placeholder': 'Enter a message'})
        return form
    
    def form_valid(self, form):
        form.instance.User = self.request.user
        form.instance.active = True
        form.save()
        messages.success(self.request, 'Your request has been created successfully!')
        return redirect(reverse_lazy('chat_commerce:request_list'))


class RequestDeleteView(LoginRequiredMixin, DeleteView):
    model = Request
    template_name = 'chat_commerce/delete_request.html'
    success_url = reverse_lazy('chat_commerce:request_list')

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Your request has been deleted successfully!')
        return redirect(reverse_lazy('chat_commerce:request_list'))
    

class OfferDeleteView(LoginRequiredMixin, DeleteView):
    model = Offer
    template_name = 'chat_commerce/delete_offer.html'
    success_url = reverse_lazy('chat_commerce:your_offers')

    def form_valid(self, form):
        self.object = self.get_object()
        self.object.delete()
        messages.success(self.request, 'Your offer has been deleted successfully!')
        return redirect(reverse_lazy('chat_commerce:your_offers'))
    


class OfferUpdateView(LoginRequiredMixin, UpdateView):
    model = Offer
    fields = ['date', 'start_time', 'end_time', 'message']
    template_name = 'chat_commerce/offer_update.html'
    
    def form_valid(self, form):
        form.save()
        messages.success(self.request, 'Your offer has been updated successfully!')
        return redirect(reverse_lazy('chat_commerce:your_offers'))