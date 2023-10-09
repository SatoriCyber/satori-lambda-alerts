# This is the only file you need to edit if your goal is
# to quick-start this AWS lambda example for Satori Cyber
# See the README for more information

# This file is part of .gitignore - for convenience and education
# purposes this file contains secrets and other sensitive information.
# You should plan on a different mechanism for storing secrets and 
# generate this file as needed. There are a few ways to do this, all
# outside the scope of this example.

# Change any value marked "FILL_IN" - if you don't change the value, 
# it's harmless and will be ignored
# e.g. if you do not use Datadog, just leave those entries alone, etc..

########################################################################
# Global Settings

# AWS Region (required)

aws_region = "us-east-1"

# The following 'handle' is used for naming conventions during terraform
# creation as well as various AWS cloud tags throughout this example
# This is a nice convenience so that you can search AWS for all resources
# in this example. (required)

satori_prefix = "SatoriPagerDutyIntegration"

# What are we reporting on?
# this lambda examples breaks out each of these types into seperate .py files
# you can thus envision creating additional reporting functionality as needed.
# the two choices are 
# a) blocked queries: reporting_type = "blockedqueries", or
# b) queries that had a large record count (>10000): reporting_type = "largerecordcount"
# see the readme for more info on these definitions (required)

reporting_type = "blockedqueries"
large_record_threshold = "5000"

# How many prior hours ago of Satori audit data will we check against?
# This is also the same value we will use when generating our AWS cloudwatch schedule
# I.e. if you are searching for the last 24 hours of audit data, you will only want to 
# run this AWS lambda example every 24 hours. (required)

hours = "24"

########################################################################
# Satori Rest API Info
# see https://app.satoricyber.com/docs/api for more info
# This section MUST be filled in, regardless of your downstream destination choices
# (required)

satori_account_id         = "FILL_IN"
satori_serviceaccount_id  = "FILL_IN"
satori_serviceaccount_key = "FILL_IN"
# Leave the following url as is unless instructed:
satori_api_url = "app.satoricyber.com"

# if nothing else below is filled in, this will be an inert alerting example but would
# still output Satori info to the Lambda Console

########################################################################
# Our PagerDuty API Configuration, see the README for more information
# general PagerDuty info: https://developer.pagerduty.com/docs
# leave as-is if not using PagerDuty

pagerduty_incident_url = "https://api.pagerduty.com/incidents"
pagerduty_apikey       = "FILL_IN"
pagerduty_service_id   = "FILL_IN"
pagerduty_sentby       = "FILL_IN"

########################################################################
# Our Datadog Events Example
# general Datadog events api info: https://docs.datadoghq.com/api/latest/events
# leave as-is if not using Datadog

dd_application_key = "FILL_IN"
dd_api_key = "FILL_IN"
datadog_url = "https://api.datadoghq.com/api/v1/events"

########################################################################
# Our Slack Channel Example
# general slack webhook info: https://api.slack.com/messaging/webhooks
# leave as-is if not using slack

slack_webhook = "FILL_IN"


# Our Generic HTTP Post Example
# COMING SOON