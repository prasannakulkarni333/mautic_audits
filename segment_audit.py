#Find the fields that segments are made of
import csv
import datetime
import json
import requests

currentDTstring = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
base_url = 'https://your_domain.net/api/segments/'
payload = ""
headers = {'Accept': "application/json"}

# replace username and password with your username & password
username = 'username'
password = 'password'

# read input csv to get segment IDs to find the fields of
file_with_input_campaign_IDs ='segmentIDs.csv'
with open(file_with_input_campaign_IDs, newline='') as f:
    reader = csv.reader(f)
    IDs = list(reader)

for ID in range(len(IDs)):
    segment_id = IDs[ID][0]
    url = base_url + segment_id
    r = requests.request("GET", url, data=payload, auth=(username, password))
    response_text = (json.loads(r.text))
    filters = response_text['list']['filters']

    with open(currentDTstring+"segmentAuditForFields.csv", 'a', newline='') as f:
        thewriter = csv.writer(f)
        length_filters=(len(filters))
        for i in range(length_filters):
            field = filters[i]['field']
            field_filter = filters[i]['properties']['filter']
            field_operator = filters[i]['operator']
            thewriter.writerow([segment_id, field, field_operator, field_filter])
