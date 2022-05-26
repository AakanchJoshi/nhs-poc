import json
import boto3

# DynamoDb table name
dynamodb_table_name = "terraform_demographics"
# Fetching DynamoDB service using boto3
dynamodb = boto3.resource("dynamodb")
# DynamoDb table
table = dynamodb.Table(dynamodb_table_name)


def buildResponse(statusCode, body=None):
    '''
    Returns the response with status code, header and body

        Parameters:
            statusCode (int): An Integer value
            body (dict): A dictionary defaults to None

        Returns:
            response (dict): response with status code, header and body
    '''
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
    '''
    Returns the patient details, if provided patientId

        Parameters:
            patientId (str): A string

        Returns:
            buildResponse (dict): buildResponse with status code, header and patient details
    '''
    response = table.get_item(Key={"patientId": patientId})

    if "Item" in response:
        return buildResponse(200, response["Item"])
    else:
        return buildResponse(404, f"Patient ID {patientId} not found")


def saveDemographics(requestBody):
    '''
    Returns the response with the success message if run successfully

        Parameters:
            requestBody (dict): consists of patientId, patientEmail, patientPhoneNo
            
        Returns:
            buildresponse (dict): buildresponse with success message (details saved)
    '''
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


def updateDemographics(patientId, updatekey, updatevalue):
    '''
    Returns the response with updated value of the field

        Parameters:
            patientId (str): A string
            updatekey (str): A field name
            updatevalue (str): Replace exixting value with new value
            

        Returns:
            buildresponse (dict): buildresponse with updated value and success message
    '''
    response = table.update_item(
        Key={
            "patientId": patientId
        },
        UpdateExpression = "SET %s = :value" % updatekey,
        ExpressionAttributeValues={
                ':value': updatevalue
        },
        ReturnValues="UPDATED_NEW"
    )
    body = {
        "message": "SUCCESS",
        "UpdatedAttrubutes": response
    }

    return buildResponse(200, body)
