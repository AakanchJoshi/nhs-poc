import json
import boto3

# DynamoDb table name
DYNAMODB_TABLE_NAME = "terraform_demographics"
# Fetching DynamoDB service using boto3
dynamodb = boto3.resource("dynamodb")
# DynamoDb table
table = dynamodb.Table(DYNAMODB_TABLE_NAME)


def build_response(status_code, body=None):
    '''
    Returns the response with status code, header and body

        Parameters:
            statusCode (int): An Integer value
            body (dict): A dictionary defaults to None

        Returns:
            response (dict): response with status code, header and body
    '''
    response = {
        "statusCode": status_code,
        "headers": {
            "Content-Type": "application/json",
            "Access-Control-Allow-Origin": "*"
        }
    }

    if body is not None:
        response["body"] = json.dumps(body)
    return response


def get_demograhics(patient_id):
    '''
    Returns the patient details, if provided patient_id

        Parameters:
            patient_id (str): A string

        Returns:
            buildResponse (dict): buildResponse with
            status code, header and patient details
    '''
    response = table.get_item(Key={"patientId": patient_id})

    if "Item" in response:
        return build_response(200, response["Item"])
    else:
        return build_response(404, f"Patient ID {patient_id} not found")


def save_demographics(request_body):
    '''
    Returns the response with the success message if run successfully

        Parameters:
            request_body (dict): consists of patientId,
            patientEmail, patientPhoneNo
        Returns:
            buildresponse (dict): buildresponse with
            success message (details saved)
    '''
    try:
        table.put_item(Item=request_body)
        body = {
            "message": "SUCCESS",
            "Item": request_body
        }
        return build_response(200, body)
    except:
        return build_response(404, "Not able to save the patient details!")


def delete_demographics(patient_id):
    '''
    Returns the response with the success message if run successfully

        Parameters:
            patient_id (str): A string

        Returns:
            buildresponse (dict): buildresponse with
            success message (details deleted)
    '''
    try:
        response = table.delete_item(Key={'patientId': patient_id})
        body = {
            "Message": "SUCCESS",
            "deleted_Item": response
        }
        return build_response(200, body)
    except:
        return build_response(404, "Not able to delete the patient details!")


def update_demographics(patient_id, updatekey, updatevalue):
    '''
    Returns the response with updated value of the field

        Parameters:
            patient_id (str): A string
            updatekey (str): A field name
            updatevalue (str): Replace exixting value
            with new value

        Returns:
            buildresponse (dict): buildresponse with updated value
            and success message
    '''
    response = table.update_item(
        Key={
            "patientId": patient_id
        },
        UpdateExpression="SET %s = :value" % updatekey,
        ExpressionAttributeValues={
                ':value': updatevalue
        },
        ReturnValues="UPDATED_NEW"
    )
    body = {
        "message": "SUCCESS",
        "UpdatedAttrubutes": response
    }

    return build_response(200, body)
