import json
import requests

def build_blockedquery_post(audit_record, pagerduty_service_id):

    payload = {"incident": {
        "type": "incident",
        "title": "Satori Audit ID " + audit_record['flow_id'],
        "service": {
            "id": pagerduty_service_id,
            "type": "service_reference"
        },
        "urgency": "high",
        "incident_key": audit_record['flow_id'],
     
        "body": {
            "type": "incident_body",
            "details": str(audit_record['identity']['name']) + 
            " tried to run the following sensitive query but it was blocked by Satori:\n\n" + 
            audit_record['query']['original_query'] +
            "\n\nfor more information: https://app.satoricyber.com/audit?timeFrame=last90days&flowId=" + 
            audit_record['flow_id']
        }
    }}

    return payload

def build_largerecords_post(audit_record, pagerduty_service_id):

    payload = {"incident": {
        "type": "incident",
        "title": "Satori Audit ID " + audit_record['flow_id'],
        "service": {
            "id": pagerduty_service_id,
            "type": "service_reference"
        },
        "urgency": "high",
        "incident_key": audit_record['flow_id'],
     
        "body": {
            "type": "incident_body",
            "details": str(audit_record['identity']['name']) + 
            " ran a query that had a larger than normal record count:\n\nRecords returned: " + 
            str(audit_record['records']['value']) +
            "\n\nfor more information: https://app.satoricyber.com/audit?timeFrame=last90days&flowId=" + 
            audit_record['flow_id']
        }
    }}

    return payload

def send_to_pagerduty(payload, pagerduty_apikey, pagerduty_incident_url, pagerduty_service_id, pagerduty_sentby):
    
    pagerduty_headers = {
        "Content-Type": "application/json",
        "Accept": "application/vnd.pagerduty+json;version=2",
        "From": pagerduty_sentby,
        "Authorization": "Token token=" + pagerduty_apikey
    }

    try:
        response = requests.request("POST", pagerduty_incident_url, json=payload, headers=pagerduty_headers)
        print("RESPONSE FROM PAGERDUTY:\n")
        print(response.json())
    except Exception as err:
        print("we are here")
        print("pager duty Exception TYPE:", type(err), Exception)
