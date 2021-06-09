import csv
import datetime
import json
import requests


csvHeader = []
current_date_string = datetime.datetime.now().strftime("%Y-%m-%dT%H:%M")

# replace username and password with your username & password
username = 'username'
password = 'password'

# replace below varaibles with html field names
check_if_dependent = 'html_name_of_field_to_check_if_dependent'
find_default_value = 'html_name_of_field_to_find_default_value_of'

# replace values in utmHiddenFields with html name of the fields you want to find matches for
fields_to_match_original = {
                            "utmHiddenFields": ["latest_lead_source", "most_recent_campaign_type", "utm_campaign_name",
                                                "most_recent_campaign", "most_recent_keyword"]
                            }

matches = []


def find_utmfields_in(form_all_fields_html_name_list):
    for i in range(len(fields_to_match_original["utmHiddenFields"])):
        if fields_to_match_original['utmHiddenFields'][i] in form_all_fields_html_name_list:
            matches.append('matchFound')
        else:
            matches.append('matchNotFound')


def html_fields_match(form_all_fields_html_name_list):
    matches.append(s1["form"]["createdByUser"])
    matches.append(s1["form"]["name"])
    matches.append(s1["form"]["dateAdded"])
    matches.append(s1["form"]["dateModified"])
    # below if statement checks for if a field is dependent
    if check_if_dependent in form_all_fields_html_name_list:
        if formFields[reveresed_form_all_fields_html_name_dict[check_if_dependent]]["parent"]:
            matches.append("is dependent")
        else:
            matches.append("is not dependent")
    else:
        matches.append("'check_if_dependent' not found on the form")

    # below if statement finds the default value of a field
    if find_default_value in form_all_fields_html_name_list:
        matches.append(formFields[reveresed_form_all_fields_html_name_dict[find_default_value]]["defaultValue"])
    else:
        matches.append("find_default_value not found on the form")

    find_utmfields_in(form_all_fields_html_name_list)


def form_audit(form_id):
    # replace below URL with URL of your instance
    base_url = 'https://your_domain.net/api/forms/'
    url = base_url + str(form_id)
    print(url)
    # replace form URL with your form URL
    form_url = "https://your_domain.com/s/forms/view/"+str(form_id)
    payload = ""
    r = requests.request("GET", url, data=payload, auth=(username, password))
    print(r.status_code)
    if r.status_code != 200:
        pass
    else:
        global s1
        s1 = json.loads(r.text)
        form_all_fields_html_name_list = []
        form_all_fields_html_name_dict = {}
        global formFields
        formFields = (s1["form"]["fields"])
        if s1["form"]["isPublished"]:
            # go through each field and get the html name
            for x in range(len(formFields)):
                # going through each field and getting values
                alias = (formFields[x]["alias"])
                # alias is the html name
                form_all_fields_html_name_list.append(alias)
                form_all_fields_html_name_dict[x]=alias
        global reveresed_form_all_fields_html_name_dict
        reveresed_form_all_fields_html_name_dict = dict(zip(form_all_fields_html_name_dict.values(), form_all_fields_html_name_dict.keys()))
        matches.append(form_url)
        html_fields_match(form_all_fields_html_name_list)
        print(form_id)


file_name = current_date_string + '_formAudit.csv'
# replace with your folder path
folder_path = 'dataFiles/'
file = folder_path+file_name

with open(file, 'a', newline='') as f:
    thewriter = csv.writer(f)
    for x in range(780, 786):
        matches = []
        form_audit(x)
        print(matches)
        thewriter.writerow(matches)
