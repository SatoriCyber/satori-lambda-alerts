import json
import requests
import datetime
import time

action_type = "ACTION_REQUEST_BLOCK" 

def get_custom_tag_audits(headers, satori_api_url, satori_account_id, hours_ago):

    # Function to retrieve Satori audit entries from the last N hours of type 'action_type'
    
    unix_endtime = int(time.time()) * 1000
    unix_starttime = (int(time.time()) - (int(hours_ago) * 3600)) * 1000
    
    # build request to rest API for audit entries, aka "data flows"
    # only search for queries which were blocked in the last 1 hour
    
    payload = {}
    auditurl = "https://{}/api/data-flow/{}/query?from={}&to={}&actionTypesFilter={}".format(
                                                                        satori_api_url,
                                                                        satori_account_id,
                                                                        unix_starttime,
                                                                        unix_endtime,
                                                                        action_type
                                                                         )
    try:
        response = requests.get(auditurl, headers=headers, data=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Retrieval of audit data failed: :", err)
        print("audit retrieval Exception TYPE:", type(err))
    else:
        print(str(response.json()['count']) + " audit records found")
        return response

def get_access_rule_request_groups(headers, satori_api_url, dataset_id):
    
    # function to get all access rules for the datasets
    
    # If any are found, then we should NOT send an alert to PagerDuty
    # because it's a false positive to assume that access was blocked
    # when in fact the end user could have the option to request access
    # using one of these access rules.
   
    url = "https://{}/api/v1/data-access-rule/access-request?parentId={}".format(satori_api_url,dataset_id)
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Retrieval of audit data failed: :", err)
        print("get access rules Exception TYPE:", type(err))
    else:
        return response

def get_access_rule_selfservice_groups(headers, satori_api_url, dataset_id):
    
    # function to get all self service rules for the datasets
    
    # If any are found, then we should NOT send an alert to PagerDuty
    # because it's a false positive to assume that access was blocked
    # when in fact the end user could have the option to request access
    # using one of these access rules.
    
    url = "https://{}/api/v1/data-access-rule/self-service?parentId={}".format(
                                                        satori_api_url,
                                                        dataset_id
                                                        )                                                     
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Retrieval of audit data failed: :", err)
        print("get self service rules Exception TYPE:", type(err))
    else:
        return response
    
def get_idp_group_by_name(headers, satori_api_url, satori_account_id, group_name):
  
    url = "https://{}/api/v1/groups?accountId={}&names={}".format(satori_api_url,satori_account_id,group_name)

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Retrieval of audit data failed: :", err)
        print("get idp groups Exception TYPE:", type(err))
    else:
        return response   


def get_local_group_by_id(headers, satori_api_url, group_id):
 
    url = "https://{}/api/v1/directory/group/{}".format(satori_apihost,group_id)
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
    except requests.exceptions.RequestException as err:
        print("Retrieval of audit data failed: :", err)
        print("get local groups Exception TYPE:", type(err))
    else:
        return response

def is_user_allowed(headers, satori_api_url, email, dataset_id):

    master_group_count = 0
    search_email = email
    target_dataset_id = dataset_id

    get_request_groups = get_access_rule_request_groups(headers, satori_api_url, target_dataset_id)
    get_selfservice_groups = get_access_rule_selfservice_groups(headers, satori_api_url, target_dataset_id)

    for group in get_request_groups.json()['records']:

        if group['identity']['identityType'] == 'USER':
            if search_email == group['identity']['identity']:
                master_group_count += 1          
        if group['identity']['identityType'] == 'EVERYONE':
            master_group_count += 1
        if group['identity']['identityType'] == 'IDP_GROUP':
            this_idp_group = get_idp_group_by_name(headers, satori_api_url, group['identity']['identity'])
            members = this_idp_group.json()['records'][0]['members']
            for item in members:
                if item['email'] == search_email:
                    master_group_count += 1
        if group['identity']['identityType'] == 'GROUP':
            this_local_group = get_local_group_by_id(headers, satori_api_url, group['identity']['identity'])
            for member in this_local_group.json()['members']:
                if member['type'] == 'USERNAME':
                    if search_email in (str(member['name']), str(member['email'])):
                        master_group_count += 1

    for group in get_selfservice_groups.json()['records']:
        if group['identity']['identityType'] == 'USER':
            if search_email == group['identity']['identity']:
                master_group_count += 1          
        if group['identity']['identityType'] == 'EVERYONE':
            master_group_count += 1
        if group['identity']['identityType'] == 'IDP_GROUP':
            this_idp_group = get_idp_group_by_name(headers, satori_api_url, group['identity']['identity'])
            members = this_idp_group.json()['records'][0]['members']
            for item in members:
                if item['email'] == search_email:
                    master_group_count += 1
        if group['identity']['identityType'] == 'GROUP':
            this_local_group = get_local_group_by_id(headers, satori_api_url, group['identity']['identity'])
            for member in this_local_group.json()['members']:
                if member['type'] == 'USERNAME':
                    if search_email in (str(member['name']), str(member['email'])):
                        master_group_count += 1

    return master_group_count    


