from collections import namedtuple

s = {"href": "https://www.vegvesen.no/nvdb/api/v2/vegobjekter/3", "id": "3", "navn": "Skjerm"}

print(s.pop('href'))
print(s)