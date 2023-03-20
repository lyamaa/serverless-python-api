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

    if "body" not in event or event["httpMethod"] != "POST":
        return {"statusCode": 400, "body": json.dumps({"error": "Bad request"})}

    coupon_table = os.environ.get("TABLE", "Coupons")
    region = os.environ.get("REGION", "ap-southeast-2")

    coupon_table = boto3.resource("dynamodb", region_name=region).Table(coupon_table)
    payload = json.loads(event["body"])
    params = {
        "id": str(uuid.uuid4()),
        "name": payload["name"],
        "couponCode": payload["couponCode"],
        "discount": payload["discount"],
        "address": payload["address"],
        "user_email": payload["user_email"],
        "dateCreated": datetime.now(timezone.utc).isoformat(),
    }

    coupon_table.put_item(Item=params)

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


# create a function publisher to publish the message using sqs
# Path: src/create_coupon/publisher.py
import boto3
import os
import json


def publish(event, context):
    """
    publish a message to the queue
    :param event:
    :param context:
    :return:
    """

    queue = os.environ.get("QUEUE", "CouponsQueue")
    region = os.environ.get("REGION", "ap-southeast-2")

    sqs = boto3.resource("sqs", region_name=region)
    # create a queue
    sqs.create_queue(QueueName=queue)
    # get the queue
    queue = sqs.get_queue_by_name(QueueName=queue)

    return queue.send_message(MessageBody=json.dumps(event))


def receive(event, context):
    """
    receive a message from the queue
    :param event:
    :param context:
    :return:
    """

    queue = os.environ.get("QUEUE", "CouponsQueue")
    region = os.environ.get("REGION", "ap-southeast-2")

    sqs = boto3.resource("sqs", region_name=region)
    # get the queue
    queue = sqs.get_queue_by_name(QueueName=queue)

    return queue.receive_messages()
