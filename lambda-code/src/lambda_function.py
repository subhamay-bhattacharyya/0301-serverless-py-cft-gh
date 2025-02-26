""" Lambda function to be used in the Serverless Patterns Lab-01"""

from typing import Dict, Any
import os
import json
from datetime import datetime
from dataclasses import dataclass

import boto3
from botocore.exceptions import ClientError, ParamValidationError
from ssm_util import get_ssm_parameter

from aws_lambda_powertools import Logger, Tracer

logger = Logger(service="serverless-lab-01")
tracer = Tracer()

ssm_client = boto3.client("ssm", region_name=os.environ["AWS_REGION"])
DYNAMODB_TABLE_NAME = get_ssm_parameter(
    ssm_client=ssm_client,
    name=f"{os.environ['PROJECT_NAME']}/{os.environ['ENVIRONMENT']}/dynamodb-table-name",
    logger=logger,
    tracer=tracer,
)


@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event, context):
    """
    AWS Lambda function handler
    """
    # Log the received event
    logger.info({"event": event})

    logger.info({"dynamoDBTableName": DYNAMODB_TABLE_NAME})

    # Process the event (example: return a greeting message)

    fake = Faker()
    users = []

    for _ in range(10):
        user = {
            "Name": fake.name(),
            "Address": fake.address().replace(
                "\n", ", "
            ),  # Replace newline characters for CSV formatting
            "Email": fake.email(),
            "Phone#": fake.phone_number(),
        }
        users.append(user)

    # Return the response
    return {"statusCode": 200, "message": "Success", "users": users}
