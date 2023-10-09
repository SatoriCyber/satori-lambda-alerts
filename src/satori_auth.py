import json
import requests

def get_token(satori_serviceaccount_id, satori_serviceaccount_key, satori_apihost):
    
    # Get a Bearer Token for all the rest of these examples
    
    auth_headers = {'content-type': 'application/json','accept': 'application/json'}
    auth_url = "https://{}/api/authentication/token".format(satori_apihost)
    auth_body = json.dumps(
    {
        "serviceAccountId": satori_serviceaccount_id,
        "serviceAccountKey": satori_serviceaccount_key
    })
    try:
        r = requests.post(auth_url, headers=auth_headers, data=auth_body)
        response = r.json()
        satori_token = response["token"]
    except Exception as err:
        print("Bearer Token Failure: :", err)
        print("bearer token Exception TYPE:", type(err))
    else:
        return {'Authorization': 'Bearer {}'.format(satori_token),}