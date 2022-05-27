import json
from demographic_functions import (build_response, get_demograhics,
                                save_demographics, delete_demographics,
                                update_demographics)

# health_path var
HEALTH_PATH = "/health"
# demographic_path var
DEMOGRAPHICS_PATH = "/demographic"


def lambda_handler(event, context):
    # httpMethod type from event
    http_method = event["http_method"]
    # path from event
    path = event["path"]

    if http_method == "GET" and path == HEALTH_PATH:
        response = build_response(200)
    elif http_method == "GET" and path == DEMOGRAPHICS_PATH:
        response = get_demograhics(event["queryStringParameters"]["patientId"])
    elif http_method == "POST" and path == DEMOGRAPHICS_PATH:
        response = save_demographics(json.loads(event["body"]))
    elif http_method == "PATCH" and path == DEMOGRAPHICS_PATH:
        request_body = json.loads(event["body"])
        response = update_demographics(request_body["patientId"],
                            request_body["updatekey"], request_body["updatevalue"])
    elif http_method == "DELETE" and path == DEMOGRAPHICS_PATH:
        body = json.loads(event["body"])
        response = delete_demographics(body["patientId"])
    else:
        response = build_response(404, "Not Found!")
    return response
