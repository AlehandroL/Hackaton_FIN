from django.urls import path

from . import views

app_name = 'chat_commerce'

urlpatterns = [
    path('', views.RequestListView.as_view(), name='request_list'),
    path('offers/', views.OfferListView.as_view(), name='offer_list'),
    path('accept_offer/', views.AcceptOffer.as_view(), name='accept_offer'),
]