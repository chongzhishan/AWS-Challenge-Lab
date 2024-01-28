#  Access a DynamoDB Table Securely from an AWS Lambda Function 

## Step 1: Create the IAM Policy
- Open the AWS Policy Generator at https://awspolicygen.s3.amazonaws.com/policygen.html.
  
Set the following values:
```
Select type of policy: IAM Policy
Effect: Allow
AWS Service: Amazon DynamoDB
Actions: All actions
Amazon Resource Name (ARN): arn:aws:dynamodb:us-east-2:*:table/scores,arn:aws:dynamodb:us-east-2:*:table/scores/index/*
```
- Click on "Add Statement" to add the policy statement.
- IAM policy named = dynamodb-scores

## Step 2: Create the IAM Policy
- Go to the IAM Management Console.
- Navigate to "Policies" and click on "Create policy."
- Choose the "JSON" tab.
- Paste the JSON document copied from the AWS Policy Generator.
- Click on "Review policy."
- Enter the name dynamodb-scores for the policy.
- Click on "Create policy."

## Step 3: Create the IAM Role
- Go to the IAM Management Console.
- Navigate to "Roles" and click on "Create role."
- Choose "Lambda" as the AWS service that will use this role.
- Click on "Next: Permissions."
- In the "Filter policies" search box, type dynamodb-scores and select the policy you created earlier.
- Also, select the AWSLambdaBasicExecutionRole.
- Click on "Next: Tags" and optionally add tags if needed.
- Click on "Next: Review."
- Enter the name lambda-scores-execution-role for the role.
- Under "Permissions boundaries," select LabSecureAccess.
- Click on "Create role."

## Step 4:  create Lambda Function
- Lambda Function name : highscores
- create a lambda_function.py
```python
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
```
- deploy highscore function
- Configure a Private test event named highscores-test for the highcores function by using the code editor and the following JSON code, and then test the event
``` JSON
{
    "queryStringParameters": {
        "game_id" : "1"
    }
}
```
Note : A JSON-formatted list of high scores for game 1 will be displayed in descending order from highest to lowest scores.

## Add a function URL to your Lambda function
- Add a function URL to the highscores Lambda function that uses None as the authentication type.
- EX : https://f2ed7jjyx3dlhrkyygp6fmbzpa0iihwv.lambda-url.us-east-2.on.aws/?game_id=1
