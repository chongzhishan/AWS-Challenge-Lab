import json
import boto3

def lambda_handler(event, context):
    ddb = boto3.client("dynamodb")
    game_id = 0
    if 'queryStringParameters' in event:
        if 'game_id' in event['queryStringParameters']:
            game_id = event['queryStringParameters']['game_id']
    else:
        game_id = event['game_id']
    resp = ddb.query(
        TableName="scores",
        IndexName="scores-index",
        KeyConditionExpression="game_id=:gameId",
        ExpressionAttributeValues={":gameId" : {"N" : game_id}},
        ScanIndexForward=False
    )
    return {
        "statusCode": 200,
        "headers": {
            "Content-Type": "application/json"
        },
        "body": json.dumps(resp['Items'])
    }