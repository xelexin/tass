import requests
re = requests.get('https://api-v3.mojepanstwo.pl/dane/krs_formy_prawne.json')
tekst = re.json()
for i in range(0,len(tekst['Dataobject'])):
    if "SPÓŁKA" in tekst['Dataobject'][i]['data']['krs_formy_prawne.nazwa']:
        print(tekst['Dataobject'][i]['id'] + " " + tekst['Dataobject'][i]['data']['krs_formy_prawne.nazwa'])