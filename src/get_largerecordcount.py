import json
import requests
import datetime
import time

import satori_auth
import satori_helpers
import post_pagerduty
import post_slack
import post_datadog

def large_record_count(event, lambda_secrets):

    headers = satori_auth.get_token(
        lambda_secrets['satori_serviceaccount_id'], 
        lambda_secrets['satori_serviceaccount_key'], 
        lambda_secrets['satori_api_url']
        )

    # 1. Get Large Records Query Audit Info

    audit_records = satori_helpers.get_large_record_query_audits(
        headers, 
        lambda_secrets['satori_api_url'], 
        lambda_secrets['satori_account_id'], 
        event['large_record_threshold'],
        event['hours']
        ).json()['records']

    # 2. Build Content and Deliver to Destinations

    for audit_record in audit_records:

        print(
            str(audit_record['identity']['name']) + 
            " ran a query with a very large record count! Records returned: " +
            str(audit_record['records']['value']))                
        

        if lambda_secrets['pagerduty_apikey'] != "FILL_IN":

            pagerduty_body = post_pagerduty.build_largerecords_post(
                audit_record, 
                lambda_secrets['pagerduty_service_id']
                )
            post_pagerduty.send_to_pagerduty(
                pagerduty_body, 
                lambda_secrets['pagerduty_apikey'], 
                lambda_secrets['pagerduty_incident_url'], 
                lambda_secrets['pagerduty_service_id'], 
                lambda_secrets['pagerduty_sentby']
                )
        
        if lambda_secrets['slack_webhook'] != "FILL_IN":
            slack_body = post_slack.build_largerecords_post(audit_record)
            post_slack.send_to_slack(
                lambda_secrets['slack_webhook'],
                slack_body
                )
    
        if lambda_secrets['dd_application_key'] != "FILL_IN":

            datadog_body = post_datadog.build_largerecords_post(audit_record)
            post_datadog.send_to_datadog(
                datadog_body,
                lambda_secrets['dd_application_key'],
                lambda_secrets['dd_api_key'],
                lambda_secrets['datadog_url']
                )
    
    print("\n")