# import os 
# import pickle
# import json
# from googleapiclient.discovery import build
# from google.auth.transport.requests import Request
# from google_auth_oauthlib.flow import InstalledAppFlow
# import google_auth_httplib2  # This gotta be installed for build() to work

# # Setup the Photo v1 API
# SCOPES = ['https://www.googleapis.com/auth/photoslibrary.readonly']
# creds = None
# if(os.path.exists("token.pickle")):
#     with open("token.pickle", "rb") as tokenFile:
#         creds = pickle.load(tokenFile)
# if not creds or not creds.valid:
#     if (creds and creds.expired and creds.refresh_token):
#         creds.refresh(Request())
#     else:
#         flow = InstalledAppFlow.from_client_secrets_file('client_secret.json', SCOPES)
#         creds = flow.run_local_server(port = 0)
#     with open("token.pickle", "wb") as tokenFile:
#         pickle.dump(creds, tokenFile)
# service = build('photoslibrary', 'v1', credentials = creds)

# # Call the Photo v1 API
# results = service.albums().list(
#     pageSize=10, fields="nextPageToken,albums(id,title)").execute()
# items = results.get('albums', [])
# if not items:
#     print('No albums found.')
# else:
#     print('Albums:')
#     for item in items:
#         print('{0} ({1})'.format(item['title'].encode('utf8'), item['id']))

import json
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import requests
SCOPES = 'https://www.googleapis.com/auth/photoslibrary.readonly'

store = file.Storage('token-for-google.json')
creds = store.get()
# creds = None
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets('client_secret.json', SCOPES)
    creds = tools.run_flow(flow, store)
google_photos = build('photoslibrary', 'v1', http=creds.authorize(Http()), static_discovery=False)

# results = gdriveservice.albums().list(
#     pageSize=10).execute()
# items = results.get('albums', [])
# for item in items:
#         print(u'{0} ({1})'.format(item['title'].encode('utf8'), item['id']))

# images = {}
nextpagetoken = 'Dummy'

if nextpagetoken != 'Dummy':
    file = open("images.json", "r")
    images = json.load(file)
    counter = len(images)
    print(counter)
else:
    images = {}
    counter = 0 


# pJi4o3Uw0J8n25LN2GN 
print()

try:
    while nextpagetoken != '':
        
        nextpagetoken = '' if nextpagetoken == 'Dummy' else nextpagetoken
        
        try:
            results = google_photos.mediaItems().list(pageSize=100, pageToken=nextpagetoken).execute()
        except:
            results = google_photos.mediaItems().list(pageSize=100, pageToken=nextpagetoken).execute()
        # results = google_photos.mediaItems().search(body={"filters":  {"dateFilter": {"dates": [{"day": '1', "month": '6', "year": '2021'}]}},
        #               "pageSize": 100, "pageToken": nextpagetoken}).execute()
        # The default number of media items to return at a time is 25. The maximum pageSize is 100.
        items = results.get('mediaItems', [])
        nextpagetoken = results.get('nextPageToken', '')
        for item in items:
            images[item['id']] = item['filename']

        # print(len(items))
        counter += len(items)
        print(f"{counter-len(items)} + {len(items)} = {counter}")
        # break
finally:
    print("next token is:", nextpagetoken)
    file = open("images.json", 'w')
    json.dump(images, file)
    file.close()