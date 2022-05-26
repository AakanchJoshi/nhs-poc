import json
from demographic_functions import (buildResponse, getDemograhics, 
                                    saveDemographics, deleteDemographics, updateDemographics)

# health_path var
health_path = "/health"
# demographic_path var
demographics_path = "/demographic"


def lambda_handler(event, context):
    # httpMethod type from event
    httpMethod = event["httpMethod"]
    # path from event
    path = event["path"]

    if httpMethod == "GET" and path == health_path:
        response = buildResponse(200)
    elif httpMethod == "GET" and path == demographics_path:
        response = getDemograhics(event["queryStringParameters"]["patientId"])
    elif httpMethod == "POST" and path == demographics_path:
        response = saveDemographics(json.loads(event["body"]))
    elif httpMethod == "PATCH" and path == demographics_path:
        request_body = json.loads(event["body"])
        response = updateDemographics(request_body["patientId"], request_body["updatekey"], request_body["updatevalue"])
    elif httpMethod == "DELETE" and path == demographics_path:
        body = json.loads(event["body"])
        response = deleteDemographics(body["patientId"])
    else:
        response = buildResponse(404, "Not Found!")
        
    return response