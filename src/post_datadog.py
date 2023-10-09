import json
import requests

def build_blockedquery_post(audit_record):
    datadog_payload = json.dumps({
            "alert_type": "warning",
            "source_type_name" : "amazon lambda",
            
            #change your Datadog event title as desired
            "title": "WARNING! BLOCKED QUERY RUN BY: " + audit_record['identity']['name'] + " at " + audit_record['flow_timestamp'], 
            
            #'original_query', 'tags' are from the original json payload from Satori
            "text": "%%% *" + audit_record['query']['original_query'] + "* \n\n\nUser Identity: " + audit_record['identity']['name'] + "\n %%%", 
            
            "tags": [
            "SATORI_AUDIT_DATA" 
          ]

        })

    return datadog_payload


def build_largerecords_post(audit_record):
    datadog_payload = json.dumps({
            "alert_type": "warning",
            "source_type_name" : "amazon lambda",
            
            #change your Datadog event title as desired
            "title": "Large Record Result Alert!! Large Amount of Records retrieved by: " + audit_record['identity']['name'] + " at " + audit_record['flow_timestamp'], 
            
            #'original_query', 'tags' are from the original json payload from Satori
            "text": "%%% *" + audit_record['query']['original_query'] + "* \n\n\nUser Identity: " + audit_record['identity']['name'] + "\n %%%", 
            
            "tags": [
            "SATORI_AUDIT_DATA" 
          ]

        })

    return datadog_payload

def send_to_datadog(payload, dd_application_key, dd_api_key, datadog_url):
    

    datadog_headers = {
      'DD-APPLICATION-KEY': dd_application_key,
      'DD-API-KEY': dd_api_key,
      'Content-Type': 'application/json'
    }

    try:
        response = requests.request("POST", datadog_url, headers=datadog_headers, data=payload)
        print(response.text)
    except requests.exceptions.RequestException as err:
        print("sending of audit data failed: :", err)
        print("Exception TYPE:", type(err))