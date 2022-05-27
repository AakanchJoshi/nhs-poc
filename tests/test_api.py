import requests
import json

url = ""

def test_getDemographics():
    data = {"patientId": "100"}
    response = requests.get(url, params=data)
    content = json.loads(response.content)
    
    assert response.status_code == 200, "Unsuccessful!"
    assert len(content["patientPhoneNo"]) == 10 , "Phone number is not correct"
    assert content["patientEmail"] == "terraform@gmail", "email is not matching!"

def test_updateDemographics(new_value="new@gmail.com"):
    data = {"patientId": "200", "updatekey": "patientEmail", "updatevalue": new_value}
    response = requests.patch(url, data=json.dumps(data))
    content = json.loads(response.content)
    email = content["UpdatedAttrubutes"]["Attributes"]["patientEmail"]
    
    assert response.status_code == 200, "Unsuccessful!"
    assert new_value is not None , "Email address has not been entered"
    assert email == new_value, "patientEmail is not matching!"
    assert email.endswith('com'), "wrong email address"

def test_deleteDemographic():
    data = {"patientId":"2"}
    response = requests.delete(url, data=json.dumps(data))
    content = json.loads(response.content)
    
    assert response.status_code == 200, "Unsuccessful"
    assert content['Message'] == "SUCCESS", "Couldn't be deleted"