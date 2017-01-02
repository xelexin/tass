import requests
import sys
import json
import _thread
import threading
# dwa typy wierzcholkow jeden to firma, drugi to czlowiek
# krawedzie nieskierowane pokazujace


def check_if_last_page(data):
    size_of_data = len(data)
    if size_of_data == download_limit:
        return False
    else:
        return True


def download_firm_data(page):
    url = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty.json?page=' + str(page) + '&limit=' + str(download_limit)
    response = requests.get(url)
    return response


def download_person_data(page):
    url = 'https://api-v3.mojepanstwo.pl/dane/krs_osoby.json?page=' + str(page) + '&limit=' + str(download_limit)
    response = requests.get(url)
    return response


def download_firm_id_data(number):
    url = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty/'+str(number)+'.json'
    response = requests.get(url)
    return response


def download_firm():
    dane = download_firm_data(1)
    # print(json.dumps(json.loads(dane), sort_keys=True, indent=2))
    next_page = dane.json()["Links"]["next"].split("=")[1].split("&")[0]
    last_page = dane.json()["Links"]["last"].split("=")[1].split("&")[0]
    for i in range(1, 1001):
        dane = download_firm_data(i)
        data = dane.json()["Dataobject"]
        for j in range(0, len(data)):
            idfirm = data[j]["id"]
            namefirm = data[j]["data"]["krs_podmioty.firma"]
            firms[idfirm] = namefirm
        sys.stdout.write("\rPobieranie firm: {0}/{1}".format(i, last_page))
        sys.stdout.flush()
    print('')


def download_firm_by_id(start, end):
    firms = {}
    for i in range(int(start), int(end)):
        sys.stdout.write("\rPobieranie firm: {0}/{1}".format(i, end))
        sys.stdout.flush()
        dane = download_firm_id_data(i)
        dane = dane.json()
        if 'name' in dane:
            continue
        firms[i] = str(dane)
    save_dictionary(firms, "firms_id_"+str(start)+"_"+str(end))


def download_person():
    persons = {}
    dane = download_person_data(1)
    # print(json.dumps(json.loads(dane), sort_keys=True, indent=2))
    next_page = dane.json()["Links"]["next"].split("=")[1].split("&")[0]
    last_page = dane.json()["Links"]["last"].split("=")[1].split("&")[0]
    #for i in range(1, int(last_page)+1):
    for i in range(1, 999):
        dane = download_person_data(i)
        data = dane.json()["Dataobject"]
        for j in range(0, len(data)):
            idperson = data[j]["id"]
            nameperson = data[j]["data"]["krs_osoby.imiona"] + " " + data[j]["data"]["krs_osoby.nazwisko"]
            persons[idperson] = nameperson
        sys.stdout.write("\rPobieranie osob: {0}/{1}".format(i, last_page))
        sys.stdout.flush()
    print('')
    return persons


def save_dictionary(dict, filename):
    target = open(filename, 'w')
    target.write(str(dict))
    target.close()


def read_dictionary(filename):
    dict = open(filename, 'r').read()
    return eval(dict)


def run_download_firm():
    size = 800000
    threads = 64
    sizeofdownload = size/threads
    print("Size of one download: "+str(sizeofdownload))
    # sizeofdownload = 10
    #download_firm_by_id(0,10)
    for i in range(0, threads):
        #thread.start_new_thread(download_firm_by_id(), (i*sizeofdownload, (i+1)*sizeofdownload))
        try:
            # _thread.start_new_thread(download_firm_by_id, (0*i, 10*i))
            absc = threading.Thread(target=download_firm_by_id, args=(sizeofdownload*i, sizeofdownload*(i+1)))
            absc.start()
        except Exception as e:
            import traceback
            traceback.format_exc()
            print(e)





#download_limit = 1000
#firms = {}
#download_firm()
# save_dictionary(firms, "firmy.dat")
#firms = read_dictionary("firmy.dat")
#print(len(firms))
#print(max(firms.keys(), key=int))

#firms = download_firm_by_id()
#print(len(firms))
#save_dictionary(firms, "firmyid.dat")
run_download_firm()

#persons = download_person()
#save_dictionary(persons, "ludzie.dat")
#persons = read_dictionary("ludzie.dat")
#print(len(persons))

#print(max(persons.keys(), key=int))
