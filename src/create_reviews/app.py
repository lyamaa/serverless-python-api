import boto3
import os
import json
import uuid
from datetime import datetime, timezone


def lambda_handler(event, context):
    """
    create a reviews in the reviews table
    :param event:
    :param context:
    :return:
    """
    if "body" not in event or event["httpMethod"] != "POST":
        return {"statusCode": 400, "body": json.dumps({"error": "Bad request"})}

    table_name = os.environ.get("TABLE", "Reviews")
    region = os.environ.get("REGION", "ap-southeast-2")

    review_table = boto3.resource("dynamodb", region_name=region).Table(table_name)
    payload = json.loads(event["body"])
    params = {
        "id": str(uuid.uuid4()),
        "questionsAndAnswers": dict(payload)["questionsAndAnswers"],
        "name": payload["name"],
        "userName": payload["userName"],
        "email": payload["email"],
        "address": payload["address"],
        "openData": payload["openData"],
        "imageurl": payload["imageurl"],
        "totalPoints": payload["totalPoints"],
        "dateCreated": datetime.now(timezone.utc).isoformat(),
    }

    review_table.put_item(Item=params)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token,accessKeyId,secretAccessKey",
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Credentials": "true",
            "Access-Control-Allow-Methods": "POST",
            "Content-Type": "application/json",
        },
        "body": json.dumps({"message": "Review created successfully"}),
    }
