import json
import requests

def send_to_pagerduty(flow_id, user, query, pagerduty_apikey, pagerduty_incident_url, pagerduty_service_id, pagerduty_sentby):
    
    # Function to send Satori Audit Data to PagerDuty
    
    # We kept our PagerDuty POST payload to a bare minimum
    # You need to look up the Service ID from PagerDuty
    # For the PagerDuty incident_key we reuse the Satori Audit ID which is a great convenience!
    
    # From Satori, we pulled the audit id (flow_id), user email, and query that was run
    # There is a wealth of additional information you can send from Satori to PagerDuty.
    # see https://app.satoricyber.com/docs/api#get-/api/data-flow/-accountId-/query
    
    payload = {"incident": {
        "type": "incident",
        "title": "Satori Audit ID " + flow_id,
        "service": {
            "id": pagerduty_service_id,
            "type": "service_reference"
        },
        "urgency": "high",
        "incident_key": flow_id,
     
        "body": {
            "type": "incident_body",
            "details": user + " tried to run the following sensitive query but it was blocked by Satori:\n\n" + query
        }
    }}

    pagerduty_headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "From": pagerduty_sentby,
        "Authorization": "Token token=" + pagerduty_apikey
    }

    try:
        response = requests.request("POST", pagerduty_incident_url, json=payload, headers=pagerduty_headers)
        print(response.json())
    except Exception as err:
        print("pager duty Exception TYPE:", type(err))
