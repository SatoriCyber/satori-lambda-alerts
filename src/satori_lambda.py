import json
import requests
import datetime
import time

import satori_auth
import satori_helpers
import satori_pagerduty
import satori_secrets


def lambda_handler(event, context):

    lambda_secrets = satori_secrets.get_secrets(event['secret_name'], event['aws_region'])

    hours_ago = event['hours']
    
    satori_account_id = lambda_secrets['satori_account_id']
    satori_serviceaccount_id = lambda_secrets['satori_serviceaccount_id']
    satori_serviceaccount_key = lambda_secrets['satori_serviceaccount_key']
    satori_api_url = lambda_secrets['satori_api_url']
    pagerduty_incident_url = lambda_secrets['pagerduty_incident_url']
    pagerduty_apikey = lambda_secrets['pagerduty_apikey']
    pagerduty_service_id = lambda_secrets['pagerduty_service_id']
    pagerduty_sentby = lambda_secrets['pagerduty_sentby']

    satori_token = satori_auth.get_token(satori_serviceaccount_id, satori_serviceaccount_key, satori_api_url)
    headers = {'Authorization': 'Bearer {}'.format(satori_token),}

    for item in satori_helpers.get_custom_tag_audits(headers, satori_api_url, satori_account_id, hours_ago).json()['records']:
        flow_id = str(item['flow_id'])
        user = str(item['identity']['name'])
        query = str(item['query'])
        datasets = item['datasets']
        total_rule_count = 0
        for dataset in datasets:
            # if you are testing and don't get a PagerDuty incident created
            # it means the Satori dataset associated with the audit ID has one or
            # more access rules and self-service rules defined

            # if is_user_allowed() returns 0, it means there are no rules that would allow this user
            # to access this data, which thus deserves a pagerDuty incident!!
                
            rules_found = satori_helpers.is_user_allowed(headers, satori_api_url, user, dataset['dataset_id'])
            if rules_found == 0:
                print("dataset_id: " + dataset['dataset_id'] + ": rules found (" + str(rules_found) + ") for user " + user + ":\nSENDING PAGERDUTY ALERT")                
                satori_pagerduty.send_to_pagerduty(flow_id, user, query, pagerduty_apikey, pagerduty_incident_url, pagerduty_service_id, pagerduty_sentby)
            else:
                print("dataset_id: " + dataset['dataset_id'] + ": rules found (" + str(rules_found) + ") for user " + user + ":\nWILL NOT SEND a pagerduty alert")
            print("\n")

