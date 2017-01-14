import networkx as nx
import ast
import sys

def read_dictionary(filename):
    dict = open(filename, 'r').read()
    return eval(dict)

def add_people_to_graph():
    people = read_dictionary("ludzie")
    ilosc_ludu = len(people)
    i = 1
    for key in people.keys():
        sys.stdout.write("\rPostep dodawania ludzi do grafu: {0}/{1}".format(i, ilosc_ludu))
        sys.stdout.flush()
        temp = ast.literal_eval(people[key])
        insert_data= {}
        insert_data['imiona'] = temp['imiona']
        insert_data['data_urodzenia'] = temp['data_urodzenia']
        insert_data['nazwisko'] = temp['nazwisko']
        G.add_node("osoba" + key, dane=str(insert_data))
        i += 1
    print("")


def add_firms_to_graph(firms):
    ilosc_firm = len(firms)
    i = 1
    for key in firms.keys():
        sys.stdout.write("\rPostep dodawania firm do grafu: {0}/{1}".format(i, ilosc_firm))
        sys.stdout.flush()
        temp = ast.literal_eval(firms[key])
        insert_data = {}
        insert_data['nazwa'] = temp['nazwa']
        insert_data['forma'] = temp['forma']
        insert_data['firmy'] = temp['firmy']
        G.add_node("podmiot"+key, dane = str(insert_data))
        i+=1
        # if temp['graph']['relationships'] != []:
        #     print("")
        #     print(temp['graph']['relationships'][0])
        #     exit()
    print("")


def add_edges(firms):
    ilosc_firm = len(firms.keys())
    # edges_count = get_relations_count(firms)0

    x=1
    for key in firms.keys():
        sys.stdout.write("\rPostep dodawania krawedzi do grafu: {0}/{1}".format(x, ilosc_firm))
        sys.stdout.flush()
        temp = ast.literal_eval(firms[key])
        edge_data = temp['graph']['relationships']
        for j in range(0,len(edge_data)):
            G.add_edge(edge_data[j]['start'],edge_data[j]['end'])
        udzialy = temp['firmy']
        for j in range(0,len(udzialy)):
            temp1 = udzialy[j]
            udzial = temp1['id']
            G.add_edge("podmiot"+key,"podmiot"+udzial)
        x+=1
    print("")

G = nx.Graph()
add_people_to_graph()
print("Bozy lud dodany do grafu")
firms = read_dictionary("firmy")
add_firms_to_graph(firms)
print("Liczba wierzcholkow po zaladowaniu osob i firm: "+ str(len(G.nodes())))

add_edges(firms)
nx.write_gml(G,"spolkizudzialami.gml.gz")

print(len(G.edges()))
