# satori-lambda-alerts
A collection of AWS Lambda Examples for sending alerts to downstream system using Satori audit data.

#### Quick Start

Requirements:

- You are an AWS admin who can retrieve and use CLI credentials
- You have terraform deployed on your client 
- (we tested the above with MacOS)
- You have a PagerDuty account configured, including a Rest API Key. Specifically, you have:
	- pagerduty_incident_url = "https://api.pagerduty.com/incidents"
	- pagerduty_apikey = "MUST_FILL"
	- pagerduty_service_id = "MUST_FILL"
	- pagerduty_sentby = "youremail@yourcompany.com"

#### Steps

- Download this repo
- get your AWS CLI credentials and paste them into a CLI session
- edit ```terraform.tfvars``` will all relevent info
- deploy using ```terraform apply```

#### Expected Behavior

If everything was configured and you left the default 'hours=24', then when this lambda function runs once a day, it will find all queries in the trailing 24 hours which were BLOCKED by Satori. It will then reduce this list to only those queries for which **no requestable rules were found** for the user, the Satori Dataset, and its various possible rules. (Because, blocked queries where the end user can request access are a kind of false positive and should not be part of this example).

For each remaining query that was truly blocked, this lambda function will then send an alert to PagerDuty.

#### Note About ```terraform.tfvars``` and secrets

We didn't get into the nuance of where to store your secrets - there are a handful of ways to handle this correctly. This example ships with an empty terraform.tfvars file and it is expected that you will place your sensitive info here. From there, this terraform example will create a proper AWS secret using AWS Secret Manager, assign the correct permissions, etc.