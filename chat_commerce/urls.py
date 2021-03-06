from django.urls import path

from . import views, viewAcceptOffer

app_name = 'chat_commerce'

urlpatterns = [
    path('', views.RequestListView.as_view(), name='request_list'),
    path('offered_to_you/', views.OfferedToYou_ListView.as_view(), name='offerred_to_you'),
    path('your_offers/', views.YourOffers_ListView.as_view(), name='your_offers'),
    path('accept_offer/<int:offerId>/', viewAcceptOffer.accept_offer, name='accept_offer'),
    path('make_offer/<int:id>/', views.OfferCreateView.as_view(), name='make_offer'),
    path('make_request/', views.RequestCreateView.as_view(), name='make_request'),
    path('delete_request/<pk>', views.RequestDeleteView.as_view(), name='delete_request'),
    path('delete_offer/<pk>', views.OfferDeleteView.as_view(), name='delete_offer'),
    path('offer_update/<pk>', views.OfferUpdateView.as_view(), name='offer_update'),
]