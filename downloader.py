import requests
import sys
import threading
import os.path
import ast
import json
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
    url = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty/'+str(number)+'.json?layers[]=firmy&layers[]=graph'
    response = requests.get(url, timeout=None)
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
        url = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty/' + str(i) + '.json?layers[]=firmy&layers[]=graph'
        try:
            dane = requests.get(url, timeout=10)
        except:
            print("\nBlad pobrania id: "+str(i))
            dane = "blad_pobrania"
            firms[i] = str(dane)
            continue
        dane = dane.json()
        if 'name' in dane:
            dane = "wywalilo"
        firms[i] = str(dane)
    save_dictionary(firms, "firms_id_"+str(start)+"_"+str(end))


def download_person_by_id(start, end):
    firms = {}
    for i in range(int(start), int(end)):
        sys.stdout.write("\rPobieranie ludzi: {0}/{1}".format(i, end))
        sys.stdout.flush()
        url = 'https://api-v3.mojepanstwo.pl/dane/krs_osoby/' + str(i) + '.json'
        try:
            dane = requests.get(url, timeout=10)
        except:
            print("\nBlad pobrania id: "+str(i))
            dane = "blad_pobrania"
            firms[i] = str(dane)
            continue
        dane = dane.json()
        if 'name' in dane:
            dane = "wywalilo"
        firms[i] = str(dane)
    save_dictionary(firms, "people_id_"+str(start)+"_"+str(end))


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


def run_download_people():
    size = 1700032
    threads = 64
    sizeofdownload = size/threads
    print("Size of one download: "+str(sizeofdownload))
    for i in range(0, threads):
        try:
            absc = threading.Thread(target=download_person_by_id, args=(sizeofdownload*i, sizeofdownload*(i+1)))
            absc.start()
        except Exception as e:
            import traceback
            traceback.format_exc()
            print(e)


def run_download_firm_again():
    size = 800000
    threads = 16
    sizeofdownload = size/threads
    for i in range(0, threads):
        if os.path.isfile("firms_id_"+str(sizeofdownload*i)+"_"+str(sizeofdownload*(i+1))):
            print("firms_id_"+str(sizeofdownload*i)+"_"+str(sizeofdownload*(i+1))+" istnieje")
        else:
            print("firms_id_"+str(sizeofdownload*i)+"_"+str(sizeofdownload*(i+1))+" nie ma")
            print("odpalam watek")
            try:
                absc = threading.Thread(target=download_person_by_id, args=(sizeofdownload*i, sizeofdownload*(i+1)))
                absc.start()
            except Exception as e:
                import traceback
                traceback.format_exc()
                print(e)


def download_lacks(suffix):
    size = 800000
    threads = 64
    sizeofdownload = size / threads
    print("siema")
    for i in range(0, threads):
        start = sizeofdownload*i
        end = sizeofdownload*(i+1)
        print("firms_id_" + str(start) + "_" + str(end) + "pelny.txt")
        firms_file = "firms_id_" + str(start) + "_" + str(end)+ "pelny.txt"
        if os.path.isfile(firms_file):
            firmy={}
            firms = read_dictionary(firms_file)
            for key, value in firms.items():
                if value == "blad_pobrania":
                    url = 'https://api-v3.mojepanstwo.pl/dane/krs_podmioty/' +str(key)+ '.json?layers[]=firmy&layers[]=graph'
                    #url = 'https://api-v3.mojepanstwo.pl/dane/krs_osoby/' + str(key) + '.json'
                    try:
                        print(url)
                        dane = requests.get(url, timeout=10)
                    except:
                        print("\nBlad pobrania id: " + str(key))
                        dane = "blad_pobrania"
                        firmy[i] = str(dane)
                        continue
                    dane = dane.json()
                    if 'name' in dane:
                        dane = "wywalilo"
                    firmy[key] = str(dane)
                else:
                    firmy[key] = firms[key]

            print("Zapisuje pod nazwa: "+firms_file+suffix)
            save_dictionary(firmy, firms_file+suffix)
            firms.clear()
            firmy.clear()


def check_lacks(suffix):

    sizeofdownload = size / threads
    print("siema")
    for i in range(0, threads):
        start = sizeofdownload * i
        end = sizeofdownload * (i + 1)
        print("firms_id_" + str(start) + "_" + str(end)+suffix)
        firms_file = "firms_id_" + str(start) + "_" + str(end) + suffix
        if os.path.isfile(firms_file):
            i=0
            firms = read_dictionary(firms_file)
            print(str(list(firms.keys())[0]))
            for key, value in firms.items():
                if value == "blad_pobrania":
                    i += 1
            print("Nie pobrano: "+str(i))


def load_all_firms(suffix, endfilename):
    sizeofdownload = firms_size/firms_threads
    concatenate_firms = {}
    for i in range(0, firms_threads):
        start = sizeofdownload*i
        end = sizeofdownload*(i+1)
        firms_file = "firms_id_" + str(start) + "_" + str(end) + "" + suffix
        # print(firms_file)
        if os.path.isfile(firms_file):
            sys.stdout.write("\rLadowanie pliku: {0}/{1}".format(i, firms_threads))
            sys.stdout.flush()
            firms = read_dictionary(firms_file)
            for key, value in firms.items():
                if key in concatenate_firms:
                    sys.exit("klucz istnieje")
                elif value == "blad_pobrania":
                    sys.exit(str(key) + " nie pobrany?")
                elif value == "wywalilo":
                    continue
                else:
                    concatenate_firms[key] = value
        else:
            print("Error")
    # print(len(concatenate_firms))
    print("")
    #save_dictionary(concatenate_firms, endfilename)
    return concatenate_firms


def load_all_people(suffix):
    sizeofdownload = people_size/people_threads
    concatenate_people = {}
    for i in range(0, people_threads):
        start = sizeofdownload*i
        end = sizeofdownload*(i+1)
        people_file = "people_id_" + str(start) + "_" + str(end) + "" + suffix
        if os.path.isfile(people_file):
            sys.stdout.write("\rLadowanie pliku: {0}/{1}".format(i, people_threads))
            sys.stdout.flush()
            people_dict = read_dictionary(people_file)
            for key, value in people_dict.items():
                if key in concatenate_people:
                    print(key)
                    print(value)

                    sys.exit("klucz istnieje")
                elif value == "blad_pobrania":
                    sys.exit(str(key) + " nie pobrany?")
                elif value == "wywalilo":
                    continue
                else:
                    concatenate_people[key] = value
        else:
            print("Error")
    # print(len(concatenate_firms))
    print("")
    #save_dictionary(concatenate_firms, endfilename)
    return concatenate_people

def create_short_file_people(filename):
    people = load_all_people("pelny.txt.dat")
    print(len(people))
    output={}
    for key, value in people.items():
        sys.stdout.write("\rZapisywanie wyniku: {0}".format(key))
        sys.stdout.flush()
        temp = ast.literal_eval(value)['data']
        temp1 = {}
        temp1['id'] = temp['krs_osoby.id']
        temp1['imiona'] = temp['krs_osoby.imiona']
        temp1['nazwisko'] = temp['krs_osoby.nazwisko']
        temp1['data_urodzenia'] = temp['krs_osoby.data_urodzenia']
        output[temp1['id']] = str(temp1)
    save_dictionary(output,filename)

def create_short_file_firm(filename):
    firms = load_all_firms("pelny.txt.dat","wszystkie_firmy")
    print(len(firms))
    formy_prawne = ['10','11','12','13','14','32','38']
    output={}
    for key,value in firms.items():
        sys.stdout.write("\rZapisywanie wyniku: {0}".format(key))
        sys.stdout.flush()
        temp = ast.literal_eval(value)
        # print(temp)
        # print(temp['krs_podmioty.forma_prawna_id'])
        if temp['data']['krs_podmioty.forma_prawna_id'] in formy_prawne:
            temp1 = {}
            temp1['id'] = temp['data']['krs_podmioty.id']
            temp1['nazwa'] = temp['data']['krs_podmioty.firma']
            temp1['forma'] = temp['data']['krs_podmioty.forma_prawna_id']
            temp1['graph'] = temp['layers']['graph']
            temp1['firmy'] = temp['layers']['firmy']
            output[temp['data']['krs_podmioty.id']] = str(temp1)
    save_dictionary(output,filename)

firms_size = 800000
firms_threads = 64
people_size = 1700032
people_threads = 64
# firms = load_all_firms("pelny.txt.dat","wszystkie_firmy")
# print(len(firms))

#create_short_file_people("ludzie")
create_short_file_firm("firmy_z_udzialami")

#create_one_file_firms("pelny.txt.dat","wszystkie_firmy")
#check_lacks("pelny.txt")
#download_lacks(".dat")
#firms = read_dictionary("firms_id_0.0_12500.0better.txt")
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
#run_download_firm()
#run_download_firm_again()
#persons = download_person()
#save_dictionary(persons, "ludzie.dat")
#persons = read_dictionary("ludzie.dat")
#print(len(persons))
#print(max(persons.keys(), key=int))
