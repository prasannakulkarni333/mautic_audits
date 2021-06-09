# Audit campaign to find segments that make up the campaign, events in the campaign and event properties
import csv
import datetime
import json
import requests

currentDTstring = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")
base_url = 'https://your_domain.net/api/campaigns/'
# replace username and password with your username & password
username = 'username'
password = 'password'
payload = ""
headers = {'Accept': "application/json"}

# read imput campaign IDs
file_with_input_campaign_IDs = 'Prod_OpCampaignIDs.csv'
with open(file_with_input_campaign_IDs, newline='') as f:
    reader = csv.reader(f)
    IDs = list(reader)
    print(IDs)

for ID in range(len(IDs)):
    # call the campaign url and note down campaign events, campaign
    ID = IDs[ID]
    url = base_url + (ID[0])
    r = requests.request("GET", url, data=payload, auth=(username, password))
    response_text = (json.loads(r.text))
    campaign_events = json.loads(r.text)['campaign']['events']
    campaign = json.loads(r.text)['campaign']
    campaign_lists = campaign['lists']

    # start a csv to capture segment IDs that make up the campaign
    with open(currentDTstring+"segmentsInOperationalCampaigns.csv", 'a', newline='') as f:
        thewriter = csv.writer(f)
        for i in range(len(campaign_lists)):
            segment_id = campaign_lists[i]['id']
            thewriter.writerow([ID[0], segment_id])

# capture the campaign ID, event name and event properties
    with open(currentDTstring+"propertiesInOperationalCampaigns.csv", 'a', newline='') as f:
        thewriter = csv.writer(f)
        length_campaign_events = (len(campaign_events))
        for event in range(length_campaign_events):
            event_name = campaign_events[event]['name']
            event_properties = campaign_events[event]['properties']['properties']
            thewriter.writerow([ID[0], event_name, event_properties])
