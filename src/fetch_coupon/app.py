import boto3
import os
import json
import uuid
from datetime import datetime, timezone
from decimal import *


def lambda_handler(event, context):
    """
    list all reviews in the reviews table
    """
    if "body" not in event or event["httpMethod"] != "GET":
        return {"statusCode": 400, "body": json.dumps({"error": "Bad request"})}

    table_name = os.environ.get("TABLE", "Coupons")
    region = os.environ.get("REGION", "ap-southeast-2")

    coupons_table = boto3.resource("dynamodb", region_name=region).Table(table_name)

    response = coupons_table.scan()

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": "OPTIONS,POST,GET",
        },
        "body": json.dumps(response["Items"], cls=DecimalEncoder),
    }


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        # 👇️ if passed in object is instance of Decimal
        # convert it to a string
        if isinstance(obj, Decimal):
            return str(obj)
        # 👇️ otherwise use the default behavior
        return json.JSONEncoder.default(self, obj)
