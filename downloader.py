import requests
import json
# dwa typy wierzcholkow jeden to firma, drugi to czlowiek
# krawedzie nieskierowane pokazujace

download_limit = 10
filename = 'test'


def check_if_last_page(data):
    size_of_data = len(data)
    if size_of_data == download_limit:
        return False
    else:
        return True


def download_data(page):
    url = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty.json?page=' + str(page) + '&limit=' + str(download_limit)
    response = requests.get(url)
    return response.text




print(json.dumps(json.loads(download_data(10)), sort_keys=True, indent=2))

