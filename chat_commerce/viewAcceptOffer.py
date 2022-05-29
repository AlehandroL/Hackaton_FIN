import datetime
import os.path

from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic
from django.views.generic import ListView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.template.defaultfilters import slugify
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponse
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from django.contrib.auth.models import User
from .models import Request, Offer

SCOPES = ['https://www.googleapis.com/auth/calendar']

def accept_offer(receivedRequest, offerId):
    offer = Offer.objects.get(pk=offerId)
    request = Request.objects.get(pk=offer.id)
    #requestUser = Request.User
    offerUser = offer.User
    print(offerUser.email)

    user = User.objects.get(id=2)
    user_email = user.email
    #print ('requestUser: '+ requestUser.email)
    print ('offerUser: '+ str(offerUser))

    #print(f'hola {self.Request.User.username}')
    event = {
        'summary': 'Chat: Ignacio',
        'description': 'Hora de chat de servicio al cliente.',
        'start': {
            'dateTime': ''+str(offer.date)+'T'+str(offer.start_time)+'-04:00',
            'timeZone': 'America/Santiago',
        },
        'end': {
            'dateTime': ''+str(offer.date)+'T'+str(offer.end_time)+'-04:00',
            'timeZone': 'America/Santiago',
        },
        'attendees': [
            {'email': 'iaheck@uc.cl'},
            {'email': ''+offerUser.email+''},
        ]
    }
    
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    #if os.path.exists('token.json'):
    #    creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()

    except HttpError as error:
        print('An error occurred: %s' % error)

    print ('Event created: %s' % (event.get('htmlLink')))
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")
