## **Record the API Gateway Invocation URL and API Key:**
   - Record the API Gateway Invocation URL of the API Gateway resource named `highscores` in the API named `scores`.
   - Record the value of the API key `dev-key` associated with the API.
## **Test the API Gateway:**
   - Open AWS CloudShell.
   - Run the provided cURL commands to test the API Gateway endpoint:
     ```bash
     curl -H "x-api-key: <APIKey>" <APIGatewayURL>?game_id=1 
     ```
     Make sure the response body contains a list of high scores in JSON format.
   - Run the following cURL command without using the API key:
     ```bash
     curl <APIGatewayURL>?game_id=1 
     ```
     Confirm that the response body displays a key message with a value of "forbidden".

## **Create and Deploy the Lambda Function:**
   - Create a new Lambda function named `putscores`.
   - Use the latest version of Python.
   - Attach the `DE1001-LambdaRole-Highscores` IAM role to the Lambda function.
   - Copy and paste the provided Python code into the Lambda function.
```python
import json
import boto3

def lambda_handler(event, context):
    resp = {
        "statusCode": 200,
        "body": {}
    }
    client = boto3.client('dynamodb')
    # Differentiate between the test event - which comes through as a JSON object - and the 
    # API Gateway execution, which is a string and needs to be converted to JSON 
    # using json.loads(). 
    inputObj = event["body"]
    if isinstance(inputObj, str):
        inputObj = json.loads(inputObj)
    print(inputObj)
    # Validate input. 
    allValuesExist = "game_id" in inputObj and "player_id" in inputObj and "date" in inputObj and "top_score" in inputObj
    if not allValuesExist: 
        resp["statusCode"] = 400
        resp["body"] = {"error": "Not all attributes exist. Attributes required: game_id, player_id, date, top_score"}
        return json.dumps(resp)
    try:     
        db_response = client.put_item(
            TableName="scores",
            Item={
                "game_id": {
                    'N': inputObj["game_id"]
                },
                "player_id": {
                    'S': inputObj["player_id"]
                },
                "date": {
                    'S': inputObj["date"]
                },
                "top_score": {
                    'N': inputObj["top_score"]
                }
            }
        )
    except Exception as ex:
        resp["statusCode"] = 400
        resp["body"] = json.dumps({ "Error":  str(ex)})
        return resp
    print(db_response)
    resp["statusCode"] = db_response['ResponseMetadata']['HTTPStatusCode']
    if resp['statusCode'] == 200:
        resp["body"] = json.dumps({"confirmationId" : db_response["ResponseMetadata"]["HTTPHeaders"]["x-amzn-requestid"]})
    return resp
```

##  Create and Run a Test Event:

- Create a test event named `putscores-test` with Private event sharing settings.
- Use the provided JSON payload for the test event:
    ```json
    {
        "body": {
            "player_id": "player12",
            "game_id": "1",
            "date": "2023-04-03T00:06:34Z",
            "top_score": "10192"
        }
    }
    ```
- Run the test event.
- Verify that the response body has a StatusCode value of 200.

## Verify DynamoDB Record:

- Verify that a new record for `player12` has been added to the DynamoDB `scores` table.
- Check that 11 items are displayed, including the new item for `player12`.

## Add a PUT Method to the API Gateway Resource:

- Navigate to the API Gateway console.
- Go to the `scores` API.
- Select the `highscores` resource.
- Click on the `Actions` dropdown menu and choose `Create Method`.
- Choose `PUT` from the dropdown menu and click on the checkmark button.
- In the `Integration type` dropdown, choose `Lambda Function`.
- Select the Region where your Lambda function (`putscores`) resides.
- Type the name of the Lambda function (`putscores`) and select it from the dropdown.
- Check the box for `Use Lambda Proxy integration`.
- Under `API Key Required`, check the box and select `dev-key`.
- Click on `Save`.

## Test the New Method:

- In the API Gateway console, select the `PUT` method under the `highscores` resource.
- Go to the `Method Execution` screen.
- Click on `Test`.
- In the `Request Body` section, paste the provided JSON payload:
    ```json
    {
        "player_id": "player12",
        "game_id": "1",
        "date": "2023-04-03T00:06:34Z",
        "top_score": "10192"
    }
    ```
- Click on `Test`.

## Deploy Changes to the dev Stage:

- In the API Gateway console, go to the `Actions` dropdown menu and choose `Deploy API`.
- Select the `dev` stage and click on `Deploy`.
- Note the deployed API URL.

## Test the API Endpoint Using cURL:

- Open AWS CloudShell.
- Run the following cURL command to call the API endpoint:
    ```bash
    curl -X PUT -H "x-api-key: Pa3B7SasNZ8xVws7dXS1a1ihFToYVL916ExKzMoY" -d '{"player_id": "player12","game_id": "1","date": "2023-04-03T00:06:34Z","top_score": "10192"}' https://c7p3va8z7b.execute-api.us-east-2.amazonaws.com
    ```
- Verify that you receive a JSON response containing a `confirmationId` property.

## Create a New Stage Named "test":

- Navigate to the API Gateway console.
- Go to the `scores` API.
- Select the `/highscores` resource.
- In the `Actions` dropdown menu, choose `Deploy API`.
- Enter `test` as the stage name.
- Choose `For testing` as the description.
- Click on `Deploy`.

## Record the Test Invoke URL:

- After deploying to the `test` stage, note the Invoke URL for the `/highscores` resource from the test stage. This URL will be used for testing the API.

## Create a New Autogenerated API Key:

- In the API Gateway console, go to the `API Keys` section.
- Click on `Create API Key`.
- Choose `Autogenerated` as the API key source.
- Enter `test-key` as the name for the API key.
- Click on `Save`.

## Record the Test API Key:

- After creating the API key, note down the generated API key value. This value will be used for testing the API.

## Create a New Usage Plan:

- In the API Gateway console, go to the `Usage Plans` section.
- Click on `Create`.
- Enter `test plan` as the name for the usage plan.
- Choose `test` as the associated API stage.
- Leave throttling and quotas settings as `None`.
- Click on `Save`.

## Test the API Endpoint Using cURL:

- Open AWS CloudShell.
- Run the following cURL command to call the test API endpoint:
    ```bash
    curl -X PUT -H "x-api-key: <TestAPIKey>" -d '{"player_id": "player12","game_id": "1","date": "2023-04-03T00:06:34Z","top_score": "10192"}' <TestInvokeURL>
    ```
- Replace `<TestAPIKey>` with the test API key value and `<TestInvokeURL>` with the test Invoke URL.
- Verify that you receive a JSON response containing a `confirmationId` property.

