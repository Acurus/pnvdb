import requests
from pnvdb.var import auth

username = auth.username
password = auth.password
url = "https://datafangst.kantega.no/api/v1/contract/{contractId}/featurecollection".format(contractId='7168c19c-e637-48fd-9771-61eb43c53d6f')

payload = """{
"type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
      "geometry": {
        "type": "Polygon",
        "coordinates": [
          [ [10.39241731, 63.43053048],
            [10.39495434, 63.43043698],
            [10.39579151, 63.42898665],
            [10.39272171, 63.42909269],
            [10.39241731, 63.43053048] ]
        ]
      },
      "properties": {
        "tag": "Forsterkningslag#1",
        "dataCatalogVersion": "2.06",
        "typeId": 227,
        "comment": "Usikker på måledatoen",
        "attributes": {
          "5543": "20160802"
         }
       }
    }
  ]
}""".encode('utf8')
headers = {
    'Content-Type': "application/geo+json",
    'Accept': "application/json"}
 #'Authorization': "Basic bWFydmluLmxpbGxlaGF1Z0BrYW50ZWdhLm5vOlV0dmlrbGVya29uZmVyYW5zZQ==",
response = requests.post(url, data=payload, headers=headers,auth=(username, password))

print(response.status_code)
print(response.text)
