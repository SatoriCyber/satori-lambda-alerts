#iam and security



resource "aws_secretsmanager_secret" "satori_secret" {
  name = "${var.satori_prefix}_secrets"
}

resource "aws_secretsmanager_secret_version" "satori_secretversion" {
  secret_id     = aws_secretsmanager_secret.satori_secret.id
  secret_string = <<EOF
{
"satori_account_id": "${var.satori_account_id}",
"satori_serviceaccount_id": "${var.satori_serviceaccount_id}",
"satori_serviceaccount_key": "${var.satori_serviceaccount_key}",
"satori_api_url": "${var.satori_api_url}",
"pagerduty_incident_url": "${var.pagerduty_incident_url}",
"pagerduty_apikey": "${var.pagerduty_apikey}",
"pagerduty_service_id": "${var.pagerduty_service_id}",
"pagerduty_sentby": "${var.pagerduty_sentby}",
"slack_webhook": "${var.slack_webhook}",
"dd_application_key": "${var.dd_application_key}",
"dd_api_key": "${var.dd_api_key}",
"datadog_url": "${var.datadog_url}"
}
EOF
}



resource "aws_iam_role" "lambda_role" {
  name               = "${var.satori_prefix}_role"
  assume_role_policy = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": "sts:AssumeRole",
     "Principal": {
       "Service": "lambda.amazonaws.com"
     },
     "Effect": "Allow",
     "Sid": ""
   }
 ]
}
EOF
}
resource "aws_iam_policy" "iam_policy_for_lambda" {

  name        = "${var.satori_prefix}_policy"
  path        = "/"
  description = "Satori AWS IAM Policy for managing aws lambda role"
  policy      = <<EOF
{
 "Version": "2012-10-17",
 "Statement": [
   {
     "Action": [
       "logs:CreateLogGroup",
       "logs:CreateLogStream",
       "logs:PutLogEvents",
       "secretsmanager:GetSecretValue",
       "secretsmanager:ListSecrets"
     ],
          "Resource": [
        "arn:aws:logs:*:*:*",
        "${aws_secretsmanager_secret.satori_secret.arn}"
      ],
     "Effect": "Allow"
   }
 ]
}
EOF

}

resource "aws_iam_role_policy_attachment" "attach_iam_policy_to_iam_role" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = aws_iam_policy.iam_policy_for_lambda.arn
}