import boto3
import os
import json
import uuid
from datetime import datetime, timezone


def lambda_handler(event, context):
    """
    create a coupon code in the coupons table
    :param event:
    :param context:
    :return:
    """
    if "body" not in event or event["httpMethod"] != "DELETE":
        return {"statusCode": 400, "body": json.dumps({"error": "Bad request"})}

    coupon_table = os.environ.get("TABLE", "Coupons")
    region = os.environ.get("REGION", "ap-southeast-2")

    coupon_table = boto3.resource("dynamodb", region_name=region).Table(coupon_table)

    # delete coupons items
    item_id = event["pathParameters"]["id"]

    params = {"Key": {"id": item_id}}

    res = coupon_table.delete_item(**params)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,accessKeyId,secretAccessKey",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "POST",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": "Deleted successfully"}),
    }
