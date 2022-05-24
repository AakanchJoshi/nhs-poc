import json
import boto3

dynamodb_table_name = "demographic"
dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(dynamodb_table_name)

health_path = "/health"
demographics_path = "/demographic"


def buildResponse(statusCode, body=None):
    response = {
        "statusCode": statusCode,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }

    if body is not None:
        response["body"] = json.dumps(body)

    return response


def getDemograhics(patientId):
    response = table.get_item(Key={"patientId": patientId})

    if "Item" in response:
        return buildResponse(200, response["Item"])
    else:
        return buildResponse(404, f"Patient ID {patientId} not found")


def saveDemographics(requestBody):
    try:
        table.put_item(Item=requestBody)
        body = {
            "message": "SUCCESS",
            "Item": requestBody
        }
        return buildResponse(200, body)
    except:
        return buildResponse(404, "Not able to save the patient details!")

def deleteDemographics(patientId):
    try:
        response = table.delete_item(Key={'patientId' : patientId})
        body = {
            "Message": "SUCCESS",
            "deleted_Item" : response
        }
        return buildResponse(200, body)
    except:
        return buildResponse(404, "Not able to delete the patient details!")

def lambda_handler(event, context):
    httpMethod = event["httpMethod"]
    path = event["path"]

    if httpMethod == "GET" and path == health_path:
        response = buildResponse(200)
    elif httpMethod == "GET" and path == demographics_path:
        response = getDemograhics(event["queryStringParameters"]["patientId"])
    elif httpMethod == "POST" and path == demographics_path:
        response = saveDemographics(json.loads(event["body"]))
    elif httpMethod == "DELETE" and path == demographics_path:
        body = json.loads(event["body"])
        response = deleteDemographics(body["patientId"])
    else:
        response = buildResponse(404, "Not Found!")
        

    return response


