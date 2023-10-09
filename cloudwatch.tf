resource "aws_cloudwatch_event_rule" "satori-lambda-pagerduty-eventrule" {
  name                = "${var.satori_prefix}_eventrule"
  description         = "Schedule satori lambda pagerduty function"
  schedule_expression = "rate(${var.hours} hours)"
}

resource "aws_cloudwatch_event_target" "satori-lambda-pagerduty-eventtarget" {
  target_id = "lambda-pagerduty-function-target"
  rule      = aws_cloudwatch_event_rule.satori-lambda-pagerduty-eventrule.name
  arn       = aws_lambda_function.satori_terraform_lambda_pagerduty.arn
  input     = <<JSON
    {
      "secret_name": "${var.satori_prefix}_secrets",
      "aws_region": "${var.aws_region}",
      "reporting_type": "${var.reporting_type}",
      "hours": "${var.hours}",
      "large_record_threshold": "${var.large_record_threshold}"
    }
    JSON
}


resource "aws_lambda_permission" "allow_cloudwatch" {
  statement_id  = "AllowExecutionFromCloudWatch"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.satori_terraform_lambda_pagerduty.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.satori-lambda-pagerduty-eventrule.arn
}