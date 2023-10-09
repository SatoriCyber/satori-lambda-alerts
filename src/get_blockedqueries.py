import json
import requests
import datetime
import time

import satori_auth
import satori_helpers
import post_pagerduty
import post_slack
import post_datadog

def blocked_queries(event, lambda_secrets):


    print("getting blocked queries\n")

    headers = satori_auth.get_token(
        lambda_secrets['satori_serviceaccount_id'], 
        lambda_secrets['satori_serviceaccount_key'], 
        lambda_secrets['satori_api_url']
        )

    # 1. Get Blocked Query Audit Info

    audit_records = satori_helpers.get_blocked_query_audits(
        headers, 
        lambda_secrets['satori_api_url'], 
        lambda_secrets['satori_account_id'], 
        event['hours']
        ).json()['records']

    # 2. Build Content and Deliver to Destinations

    for audit_record in audit_records:
        total_rule_count = 0
        for dataset in audit_record['datasets']:
            # if you are testing and don't get a PagerDuty incident created
            # it means the Satori dataset associated with the audit ID has one or
            # more access rules and self-service rules defined
            # if is_user_allowed() returns 0, it means there are no rules that would allow this user
            # to access this data, which thus deserves a pagerDuty incident!!
                
            rules_found = satori_helpers.is_user_allowed(
                headers, 
                lambda_secrets['satori_account_id'], 
                lambda_secrets['satori_api_url'], 
                str(audit_record['identity']['name']), 
                dataset['dataset_id']
                )
            
            if rules_found == 0:
            
                print(
                    "dataset_id: " + dataset['dataset_id'] + 
                    ": rules found (" + str(rules_found) + 
                    ") for user " + str(audit_record['identity']['name']) + 
                    ":\nSENDING PAGERDUTY ALERT"
                    )                
                


                if lambda_secrets['pagerduty_apikey'] != "FILL_IN":

                    pagerduty_body = post_pagerduty.build_blockedquery_post(
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
                    slack_body = post_slack.build_slack_post(audit_record)
                    post_slack.send_to_slack(
                        lambda_secrets['slack_webhook'],
                        slack_body
                        )
            
                if lambda_secrets['dd_application_key'] != "FILL_IN":

                    datadog_body = post_datadog.build_blockedquery_post(audit_record)
                    post_datadog.send_to_datadog(
                        datadog_body,
                        lambda_secrets['dd_application_key'],
                        lambda_secrets['dd_api_key'],
                        lambda_secrets['datadog_url']
                        )


            else:
            
                print(
                    "dataset_id: " + dataset['dataset_id'] + 
                    ": rules found (" + str(rules_found) + ") for user " + str(audit_record['identity']['name']) + 
                    ":\nWILL NOT SEND a pagerduty alert"
                    )
            
            print("\n")

