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

def triple(s,p,o):
    '''
    Takes three arguments and adds them as an RDF truple
    :param s: subject of triple
    :param p: predicate of triple
    :param o: object of triple
    :return:
    '''
    g.add((s,p,o))

input_file = "BBa_F2620.xml"
parse_xml(input_file)


x = SBOL(input_file)
y = x.ComponentDefinitionList()
count = 1
for i in y:
    print str(count)+ ". " + str(i)
    count = count + 1
choice = int(raw_input("Choose a ComponentDefinition using numbers:"))
component_definition = y[choice-1]
print str(component_definition) + " selected."

assembly_uri = component_definition+"/assemblyplan"
triple(URIRef(assembly_uri),RDF.type,sbol_ns.AssemblyPlan)
triple(URIRef(assembly_uri),sbol_ns.type,sbol_ns.BioBrick)
x = SBOL(input_file)
parts = x.SortedChildList(component_definition)

for i in range(len(parts)-1):
    triple(URIRef(assembly_uri), sbol_ns.step, URIRef(assembly_uri+"/step"+str(i+1)))
    triple(URIRef(assembly_uri + "/step" + str(i+1)), RDF.type, sbol_ns.Step)
    triple(URIRef(assembly_uri + "/step" + str(i+1)), sbol_ns.stepnumber, Literal(str(i+1)))
    if i == 0:
        triple(URIRef(assembly_uri + "/step" + str(i+1)), sbol_ns.input, parts[i])
        triple(URIRef(assembly_uri + "/step" + str(i+1)), sbol_ns.input, parts[i+1])
        triple(URIRef(assembly_uri + "/step" + str(i+1)), sbol_ns.output, URIRef(assembly_uri+"/step"+str(i+1))+"output")
        triple(URIRef(assembly_uri + "/step" + str(i+1)), dcterms.title, Literal("Step "+str(i+1)))
    if i > 0:
        triple(URIRef(assembly_uri + "/step" + str(i + 1)), sbol_ns.input, URIRef(assembly_uri+"/step"+str(i))+"output")
        triple(URIRef(assembly_uri + "/step" + str(i + 1)), sbol_ns.input, parts[i + 1])
        triple(URIRef(assembly_uri + "/step" + str(i + 1)), sbol_ns.output, URIRef(assembly_uri+"/step"+str(i+1))+"output")
        triple(URIRef(assembly_uri + "/step" + str(i + 1)), dcterms.title, Literal("Step " + str(i + 1)))

g.serialize("addBioBrickOutput.xml")