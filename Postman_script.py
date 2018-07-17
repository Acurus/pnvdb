import requests

url = "https://datafangst-test.kantega.no/api/v1/contract/764ec77d-b53b-46c4-b8f0-cd19c94dccd8/featurecollection"

payload = "{\n\"type\": \"FeatureCollection\",\n  \"features\": [\n    {\n      \"type\": \"Feature\",\n      \"geometry\": {\n        \"type\": \"Polygon\",\n        \"coordinates\": [\n          [ [10.39241731, 63.43053048],\n            [10.39495434, 63.43043698],\n            [10.39579151, 63.42898665],\n            [10.39272171, 63.42909269],\n            [10.39241731, 63.43053048] ]\n        ]\n      },\n      \"properties\": {\n        \"tag\": \"Forsterkningslag#1\",\n        \"dataCatalogVersion\": \"2.06\",\n        \"typeId\": 227,\n        \"comment\": \"Usikker på måledatoen\",\n        \"attributes\": {\n          \"5543\": \"20160802\"\n         }\n       }\n    }\n  ]\n}"
headers = {
    'Content-Type': "application/geo+json",
    'Authorization': "Basic bWFydmluLmxpbGxlaGF1Z0BrYW50ZWdhLm5vOlV0dmlrbGVya29uZmVyYW5zZQ==",
    'Accept': "application/json"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)