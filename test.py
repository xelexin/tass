import networkx as nx
import ast
import sys

def read_dictionary(filename):
    dict = open(filename, 'r').read()
    return eval(dict)


