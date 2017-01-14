import networkx as nx
from multiprocessing import Queue
import time
G = nx.read_gml("spolkizudzialami.gml.gz")
print(len(G.edges()))
for id,data in G.nodes(data=True):
    if "podmiot" in id:
        # pobieramy wierzcholki sasiednie
        sasiedzi = G.neighbors(id)
        if sasiedzi == []:
            continue
        # w sasiedzi_ludzie znajduja sie tylko wierzcholki ktore sa osobami
        sasiedzi_ludzie = []
        # print("Sasiedzi ludzie")
        for i in range(0,len(sasiedzi)):
            if "osoba" in sasiedzi[i]:
                # print(str(sasiedzi[i]))
                sasiedzi_ludzie.append(sasiedzi[i])
        # print("Czas na polaczenia")
        polaczenia = {}
        for i in range(0, len(sasiedzi_ludzie)):
            for j in range(0, len(sasiedzi_ludzie)):
                if i == j:
                    continue
                if (sasiedzi_ludzie[i]+sasiedzi_ludzie[j] not in polaczenia) and (sasiedzi_ludzie[j]+sasiedzi_ludzie[i] not in polaczenia):
                    polaczenia[sasiedzi_ludzie[i]+sasiedzi_ludzie[j]]=1
                    if G.has_edge(sasiedzi_ludzie[i],sasiedzi_ludzie[j]):
                        # print("Istniala krawedz "+sasiedzi_ludzie[i] + " " + sasiedzi_ludzie[j])
                        G[sasiedzi_ludzie[i]][sasiedzi_ludzie[j]]['weight']+=1
                        # print("Waga tej krawedzi to "+str(G[sasiedzi_ludzie[i]][sasiedzi_ludzie[j]]['weight']))
                    else:
                        # print("Dodano krawedz "+sasiedzi_ludzie[i] + " " + sasiedzi_ludzie[j])
                        G.add_edge(sasiedzi_ludzie[i],sasiedzi_ludzie[j],weight=1)
                # else:
                    # print("Istnialo polaczenie "+sasiedzi_ludzie[i] + " " + sasiedzi_ludzie[j])

print(len(G.edges()))
nx.write_gml(G,"grafludzieludzie.gml.gz")
odwiedzone_biznesy = []
# for id,data in G.nodes(data=True):
#     if "osoba" in id:
#         if id not in odwiedzone_biznesy:
#             odwiedzone_biznesy.append(id)
# #             rozpoczyna sie przeszukiwanie wszerz
# #             tworzenie zmiennych
#             q = Queue.Queue()
#             q.put(id)
#             q.put("add")
#             multiplier = 1
#             while not q.empty():
#                 aktualny_node = q.get()
#                 if "add" in aktualny_node:
#                     multiplier += 1
#                     continue
#                 neighbors = G.







# for start,end,data in G.edges(data=True):
#     if "podmiot" in start:
#         # print("byl poejdynczy")
#         if "podmiot" in end:
#             print("mamy to!")
#             print(start)
#             print(end)
#