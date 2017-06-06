from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF
from namespaces import *
from read_sbol import SBOL, compdef2displayid, comp2partseq, compdef2comp, compdef2partseq
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

input_file = "BBa_K887000.xml"
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

assembly_method = "BioBrick"

assembly_uri = component_definition+"/assemblyplan"
triple(URIRef(assembly_uri),RDF.type,sbol_ns.AssemblyPlan)
if assembly_method == "BioBrick":
    triple(URIRef(assembly_uri),sbol_ns.type,sbol_ns.BioBrick)
    x = SBOL(input_file)
    parts = x.SortedChildList(component_definition)
    steps_list = []
    count = 0
    for i in parts:
        triple(URIRef(assembly_uri), sbol_ns["component"+str(count+1)],i)
        count = count +1
    if len(parts)%2 == 0:
        steps = len(parts) / 2
        middle = len(parts)/2
        count = 1
        output = parts[middle-1]
        for i in range(steps-1):
            # print "Step " + str(count) + ":"
            output = parts[middle-1-count], output, parts[middle-1+count]
            output = "[{}] + [{}] + [{}]".format(*output)
            steps_list.append(output)
            count = count + 1
        # print "Step " + str(count) + ":"
        steps_list.append("[{}] + [{}]".format(output, parts[count+1]))
    else:
        steps = (len(parts)-1)/2
        middle = (len(parts)+1)/2
        count = 1
        output = parts[middle - 1]
        for i in range(steps):
            output = (parts[middle-1-count], output, parts[middle-1+count])
            output = "[{}] + [{}] + [{}]".format(*output)
            steps_list.append(output)
            count = count + 1
    for i in steps_list:
        print i

if assembly_method == "Gibson":
    triple(URIRef(assembly_uri), sbol_ns.type, sbol_ns.BioBrick)
    x = SBOL(input_file)
    parts = x.SortedChildList(component_definition)
    overlap = int(raw_input("Length of overlap:"))
    new_parts = [compdef2partseq(parts[0])+compdef2partseq(parts[1])[:overlap]]
    for i in range((len(parts)-2)):
        new_parts.append(compdef2partseq(parts[i])[-overlap:]+compdef2partseq(parts[i+1])+compdef2partseq(parts[i+2])[:overlap])
    new_parts.append(compdef2partseq(parts[-2])[:-overlap]+compdef2partseq(parts[-1]))
    part_dictionary = dict(zip(parts,new_parts))