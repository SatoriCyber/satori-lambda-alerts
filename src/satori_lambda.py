import get_blockedqueries
import get_largerecordcount
import satori_secrets

def lambda_handler(event, context):

    lambda_secrets = satori_secrets.get_secrets(event['secret_name'], event['aws_region'])

    if event['reporting_type'] == "blockedqueries":
        get_blockedqueries.blocked_queries(event, lambda_secrets)

    if event['reporting_type'] == "largerecordcount":
        get_largerecordcount.large_record_count(event, lambda_secrets)