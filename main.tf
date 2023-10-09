terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.14"
    }
  }
}

provider "aws" {
  region = var.aws_region

  default_tags {
    tags = {
      Satori = "${var.satori_prefix}"
    }
  }

}




data "archive_file" "zip_the_python_code" {
  type        = "zip"
  source_dir  = "${path.module}/src/"
  output_path = "${path.module}/satori-pagerduty-lambda-python.zip"
}

resource "aws_lambda_function" "satori_terraform_lambda_pagerduty" {
  filename         = "${path.module}/satori-pagerduty-lambda-python.zip"
  source_code_hash = "${data.archive_file.zip_the_python_code.output_base64sha256}"

  function_name    = "${var.satori_prefix}_lambdafunction"
  role             = aws_iam_role.lambda_role.arn
  handler          = "satori_lambda.lambda_handler"
  runtime          = "python3.11"
  timeout          = 180
  depends_on       = [aws_iam_role_policy_attachment.attach_iam_policy_to_iam_role]
  layers           = ["arn:aws:lambda:us-east-1:336392948345:layer:AWSSDKPandas-Python311:1"]
}


