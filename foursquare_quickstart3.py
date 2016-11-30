from __future__ import print_function

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

import httplib2
import os

import urllib
import json
import time

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
                                   'foursquare-python-quickstart.json')

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

def get_using_oauth(credentials, uri, params={}):
    http = credentials.authorize(httplib2.Http())
    params['oauth_token'] = credentials.access_token
    params['v'] = '20161114'
    return http.request(uri+'?'+urllib.parse.urlencode(params))


def get_checkins(): #自身のチェックインデータの取得
    params = {'limit':'100', 'locale':'ja', 'm':'foursquare'}
    result = get_using_oauth(credentials, 'https://api.foursquare.com/v2/users/self/checkins', params)
    data = json.loads(result[1].decode('utf-8'))

    checkins = data['response']['checkins']['items']
    for checkin in checkins:
        checkin_date = time.strftime("%m/%d(%a)", time.gmtime(checkin['createdAt']))
        if checkin_date.startswith('0'):
            checkin_date = checkin_date[1:]
        checkin_date = checkin_date.replace('/0','/')
        print('%s に %s へ行きました' % (checkin_date, checkin['venue']['name']))


def get_venue_info(credentials, venue_id):   #ベニューIDを基にベニュー情報を取得
    params = {}
    result = get_using_oauth(credentials, 'https://api.foursquare.com/v2/venues/'+venue_id, params)
    data = json.loads(result[1].decode('utf-8'))

    venue_info = data['response']['venue']
    # for venue_info in venue_infos:                  #str型 venue_info
    #     print(venue_info)
    rating = venue_info.get('rating')          #レーティング  空のリストに対するエラー処理の追加が必要
    ratingSignals = venue_info.get('ratingSignals') #レーティング数かな？
    createdAt = venue_info.get('createdAt')         #ベニューの登録日
    tip = venue_info.get('tips')                    #ベニューの口コミ
    print('レーティング は %s です' % (rating))
    print('レーティング数 は %s です' % (ratingSignals))
    print('ベニュー登録日 は %s です' % (createdAt))
    print('口コミ は %s です' % (tip))
        # print(venue_info)
    # print(venue_infos)
    # print(type(venue_infos))


def search_venues(credentials): #ベニューの検索
    params = {'limit':'5','near':'熊本','query':'ラーメン'}
    result = get_using_oauth(credentials, 'https://api.foursquare.com/v2/venues/search', params)
    data = json.loads(result[1].decode('utf-8'))

    searches = data['response']['venues']   #検索に引っかかるベニュー数分の情報が格納
    for search in searches:                 #dict型 search
        id = search.get('id')               #ベニューID
        name = search.get('name')           #ベニュー名
        location = search.get('location')   #ベニューの地理情報
        category = search.get('categories') #ベニューのカテゴリ情報
        stat = search.get('stats')          #ベニューのチェックイン・ユーザ・口コミ数の情報
        get_venue_info(credentials, id)
        print()
        #確認用
        # print('ID %s は %s です' % (id, name))
        # print('ロケーション情報 は %s です' % (location))
        # print('カテゴリ情報 は %s です' % (category))
        # print('チェックイン数とかの情報 は %s です' % (stat))

    # print(searches)



if __name__ == '__main__':
    credentials = get_credentials()
    # get_checkins()
    search_venues(credentials)
