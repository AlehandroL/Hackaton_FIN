import datetime
import os.path
from datetime import timedelta
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
from django.contrib import messages

from django.contrib.auth.models import User
from .models import Request, Offer

SCOPES = ['https://www.googleapis.com/auth/calendar']

def accept_offer(receivedRequest, offerId):
    creds = get_credentials()
    send_calendar_invitation(receivedRequest, offerId, creds)
    update_offer_table(offerId)
    update_request_table(offerId)
    decline_old_calendar_event(receivedRequest, offerId, creds)
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def send_calendar_invitation(receivedRequest, offerId, creds):
    offer = Offer.objects.get(pk=offerId)
    request = Request.objects.get(pk=offer.id)
    offerUser = offer.User

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
    
    try:
        service = build('calendar', 'v3', credentials=creds)
        event = service.events().insert(calendarId='primary', body=event, sendUpdates='all').execute()

    except HttpError as error:
        print('An error occurred: %s' % error)

    print ('Event created: %s' % (event.get('htmlLink')))

    messages.success(receivedRequest, 'Your chats have been swapped successfully!')
    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def update_offer_table(offerId):
    offer = Offer.objects.get(pk=offerId)
    offer.accepted = True
    offer.active = False
    offer.save()

    requestId = Request.objects.get(original_request=offerId)
    offersToCancel = Offer.objects.filter(Request_id=requestId).filter(accepted=False)
    for offer in offersToCancel:
        print ('Deleting offer:')
        print (offer)
        offer.accepted = False
        offer.active = False
        offer.save()

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def update_request_table(offerId):
    request = Request.objects.get(original_request=offerId)
    request.accepted = True
    request.active = False
    request.save()

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def get_credentials():
    creds = None
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
    return creds

def decline_old_calendar_event(receivedRequest, offerId, creds):
    retrievedEventId = find_old_calendar_event(receivedRequest, offerId, creds)
    print (retrievedEventId)
    if retrievedEventId != '':
        try:
            service = build('calendar', 'v3', credentials=creds)
            service.events().delete(calendarId='primary', eventId=retrievedEventId).execute()
        except HttpError as error:
            print('An error occurred: %s' % error)
    else:
        print('no event to delete')

    return HttpResponse("""<html><script>window.location.replace('/');</script></html>""")

def find_old_calendar_event(receivedRequest, offerId, creds):
    offer = Offer.objects.get(pk=offerId)
    request = Request.objects.get(pk=offer.id)
    minTime = str(request.date) + 'T' + str(request.start_time) + '-04:00'
    try:
        service = build('calendar', 'v3', credentials=creds)
        events_result = service.events().list(calendarId='primary', timeMin=minTime,
                                              maxResults=1, singleEvents=True,
                                              orderBy='startTime').execute()
        events = events_result.get('items', [])

        if not events:
            print('No upcoming events found.')
            return

        for event in events:
            start = event['start'].get('dateTime', event['start'].get('date'))
            end = event['end'].get('dateTime', event['end'].get('date'))

            if (start[11:19] == str(request.start_time) and end[11:19] == str(request.end_time) and start[0:10] == str(request.date)):
                return event['id']

    except HttpError as error:
        print('An error occurred: %s' % error)
    return ''
