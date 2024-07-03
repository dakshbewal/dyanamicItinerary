import requests

# Replace with your endpoint and token
url = 'http://127.0.0.1:8000/api/all/'
token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0dXNlciIsImlzQWRtaW4iOnRydWUsImlhdCI6MTcxNjg3MjYzOSwiZXhwIjoxNzE2OTA4NjM5fQ.1DvCAp31IWLhura53A_eX6FoTvaAcYtwJs9UQOl4m-A'

headers = {
    'Authorization': token,
    'Content-Type': 'application/json'
}

data = {
    "company_id":"udanchoo",
    "quotation_id":510
    
}

response = requests.post(url, headers=headers, json=data)

print(response.status_code)
print(response.json())