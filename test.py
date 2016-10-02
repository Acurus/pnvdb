import requests

class pvdb_exeption(Exception):
    """'dette er en beskrivelse av feilen'"""
    def __init__(self, message, *args):
        self.message = 'Objekt ble ikke funnet.'




a =     {
        "code" : 4013,
        "message" : "Ukjent parameter: vegvdeling",
        "help_url" : "https://www.vegvesen.no/nvdb/api/dokumentasjon/api/page/3"
    }

http = requests.get("https://www.vegvesen.no/nvdb/api/v2/vegobjekter/87/")
for i in requests.codes:
    print(i)