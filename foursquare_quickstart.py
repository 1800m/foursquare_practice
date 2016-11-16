#!/usr/bin/env python
#coding: UTF-8

from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import datetime

#################
#追加部分
#################
import urlparse
import urllib
import urllib2
import json
import time
#################

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/calendar-python-quickstart.json
#################
# 変更部分
#################
#SCOPES = 'https://www.googleapis.com/auth/calendar.readonly'
SCOPES = ''
CLIENT_SECRET_FILE = 'foursquare_client_secret.json'
#################
APPLICATION_NAME = 'Google Calendar API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'calendar-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

#################
#追加部分
#################
def get_using_oauth(credentials, uri, params={}):
    http = httplib2.Http()
    params['oauth_token'] = credentials.access_token
    params['v'] = '20160922'
    return  http.request(uri+'?'+urllib.urlencode(params))  #Python 2.6
#    return http.request(uri+'?'+urllib.parse.urlencode(params))    #Python 3

if __name__ == '__main__':
    credentials = get_credentials()
    result = get_using_oauth(credentials, 'https://api.foursquare.com/v2/users/self/checkins',{'limit':'5'})
    data = json.loads(result[1].decode('utf-8'))
    # checkins = data['response']['checkins']['items']
    response = data['response']
    print(response)
    print(response.items())
    # for checkin in checkins:
    #     checkin_date = time.strftime("%m/%d(%a)", time.gmtime(checkin['createdAt']))
    #     if checkin_date.startswith('0'):
    #         checkin_date = checkin_date[1:]
    #     checkin_date = checkin_date.replace('/0','/')
    #     print('%s に %s へ行きました' % (checkin_date, checkin['venue']['name']))
#################

# def main():
#     """Shows basic usage of the Google Calendar API.
#
#     Creates a Google Calendar API service object and outputs a list of the next
#     10 events on the user's calendar.
#     """
#     credentials = get_credentials()
#     http = credentials.authorize(httplib2.Http())
#     service = discovery.build('calendar', 'v3', http=http)
#
#     now = datetime.datetime.utcnow().isoformat() + 'Z' # 'Z' indicates UTC time
#     print('Getting the upcoming 10 events')
#     eventsResult = service.events().list(
#         calendarId='primary', timeMin=now, maxResults=10, singleEvents=True,
#         orderBy='startTime').execute()
#     events = eventsResult.get('items', [])
#
#     if not events:
#         print('No upcoming events found.')
#     for event in events:
#         start = event['start'].get('dateTime', event['start'].get('date'))
#         print(start, event['summary'])
#
#
# if __name__ == '__main__':
#     main()
