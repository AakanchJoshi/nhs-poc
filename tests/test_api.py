import requests
import json

url = ""

def test_getDemographics():
    data = {"patientId": "100"}
    response = requests.get(url, params=data)
    content = json.loads(response.content)
    
    assert response.status_code == 200, "Unsuccessful!"
    assert content["patientEmail"] == "aakanch@outlook.com", "email is not matching!"

def test_updateDemographics(new_value="new@gmail.com"):
    data = {"patientId": "200", "updatekey": "patientEmail", "updatevalue": new_value}
    response = requests.patch(url, data=json.dumps(data))
    content = json.loads(response.content)
    email = content["UpdatedAttrubutes"]["Attributes"]["patientEmail"]
    
    assert response.status_code == 200, "Unsuccessful!"
    assert email == new_value, "patientEmail is not matching!"
