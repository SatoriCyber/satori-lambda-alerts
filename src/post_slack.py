import json
import requests

def build_slack_post(audit_record):

    message = '''
    {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Audit Alert for blocked query :rage:",
                    "emoji": true
                }
            },
        
             {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Audit ID:*\n<https://app.satoricyber.com/audit?timeFrame=last90days&flowId=%s | more info in app>"                    },
                    {
                        "type": "mrkdwn",
                        "text": "*User ID*:\n%s"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Query*:\n%s"
                    },
                                        {
                        "type": "mrkdwn",
                        "text": "*Notes*:\nThis was a blocked query for which there were no allowable access or self-service rules in place."
                    }

                ]
            }
            
        ]
    }
    ''' % (audit_record['flow_id'], audit_record['identity']['name'], audit_record['query']['original_query'])
    return message



def build_largerecords_post(audit_record):

    message = '''
    {
        "blocks": [
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": "New Audit Alert for large records query :astonished:",
                    "emoji": true
                }
            },
        
             {
                "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Audit ID:*\n<https://app.satoricyber.com/audit?timeFrame=last90days&flowId=%s | more info in app>"                    },
                    {
                        "type": "mrkdwn",
                        "text": "*User ID*:\n%s"
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Query*:\n%s"
                    },
                                        {
                        "type": "mrkdwn",
                        "text": "*Records*:\nThis query returned *%s* records!"
                    }

                ]
            }
            
        ]
    }
    ''' % (audit_record['flow_id'], audit_record['identity']['name'], audit_record['query']['original_query'],audit_record['records']['value'])
    return message

def send_to_slack(webhook, payload):
    
    headers = {'Content-Type': 'application/json'}

    try:
        response = requests.request("POST", webhook, headers=headers, data=payload)
        print(response.text)
    except Exception as err:
        print("exception in slack response TYPE:", type(err))
