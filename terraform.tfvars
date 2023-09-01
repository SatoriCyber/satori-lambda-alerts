# This is the only file you should have to change to demonstrate this example
# See the README for more information

# Our AWS Region

aws_region = "us-east-1"

# The following is used for terraform creation naming conventions and AWS cloud tags throughout this example

satori_prefix = "SatoriPagerDutyIntegration"

# How many hours of Satori audit data will we pull (for entries marked as QUERY_BLOCKED)

hours = "24"

# Satori Rest API Info

satori_account_id = "MUST_FILL"
satori_serviceaccount_id = "MUST_FILL"
satori_serviceaccount_key = "MUST_FILL"

# Leave the following url as is unless instructed:

satori_api_url = "app.satoricyber.com"

# Our PagerDuty API Configuration, see the README for more information

pagerduty_incident_url = "https://api.pagerduty.com/incidents"
pagerduty_apikey = "MUST_FILL"
pagerduty_service_id = "MUST_FILL"
pagerduty_sentby = "youremail@yourcompany.com"

# Our Slack Channel Example
# COMING SOON

# Our Datadog Events Example
# COMING SOON

# Our Generic HTTP Post Example
# COMING SOON

