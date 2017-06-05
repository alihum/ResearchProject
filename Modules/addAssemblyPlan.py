from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF
from namespaces import *
from read_sbol import SBOL
import logging

logging.basicConfig()

def parse_xml(input_file):
    """
    Parses input file to graph object
    :param input_file: input file as .xml
    :return:
    """
    global g
    g = Graph()
    g.parse(input_file)
    g.bind("pc","http://example.com/physical/#")

def triple(s,p,o):
    '''
    Takes three arguments and adds them as an RDF truple
    :param s: subject of triple
    :param p: predicate of triple
    :param o: object of triple
    :return:
    '''
    g.add((s,p,o))

input_file = "ComponentDefinitionOutput.xml"
parse_xml(input_file)

component_definition = "http://partsregistry.org/cd/BBa_F2620"
assembly_method = "BioBrick"

assembly_uri = component_definition+"/assemblyplan"
triple(URIRef(assembly_uri),RDF.type,sbol_ns.AssemblyPlan)
if assembly_method == "BioBrick":
    triple(URIRef(assembly_uri),sbol_ns.type,sbol_ns.BioBrick)
    x = SBOL(input_file)
    parts = x.SortedChildList()
    count = 0
    for i in parts:
        triple(URIRef(assembly_uri), sbol_ns["component"+str(count+1)],i)
        count = count +1

g.serialize("Output.xml")