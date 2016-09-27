"""import requests

baseUrl = 'https://www.vegvesen.no/nvdb/api/v2/vegobjekter/45'

payload = {'inkluder':'metadata,egenskaper'}

r = requests.get(baseUrl,params=payload)
print(r.url)"""
segmentation = 'true'
srid = '32633'
params = {'antall':'2'}

b = {'segmentering':segmentation,'srid':srid}
params.update(b)
print(params)
