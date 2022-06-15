from email import message
import boto3
import os
import json
from decimal import *

from boto3.dynamodb.conditions import Key


def lambda_handler(event, context):  # sourcery skip: avoid-builtin-shadow
    """
    filter reviews in the reviews table
    """

    if "queryStringParameters" not in event or event["httpMethod"] != "GET":
        return {"statusCode": 400, "body": json.dumps({"error": "Bad request"})}

    table_name = os.environ.get("TABLE", "Reviews")
    region = os.environ.get("REGION", "ap-southeast-2")

    review_table = boto3.resource("dynamodb", region_name=region).Table(table_name)

    filter_by_name = event["queryStringParameters"].get("name")

    response = review_table.scan(FilterExpression=Key("name").eq(filter_by_name))

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
