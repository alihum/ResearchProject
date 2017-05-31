from rdflib import Namespace, Graph
from rdflib.namespace import RDF
from read_sbol import comp2compdef, compdef2displayid, comp2range, compdef2comp

input_file = "BBa_P0440.xml"
g = Graph()
g.parse(input_file)

sbol_ns = Namespace("http://sbols.org/v2#")
myapp = Namespace("http://myapp.com/")
prov = Namespace("http://www.w3.org/ns/prov#")
dcterms = Namespace("http://purl.org/dc/terms/")

cd_list = []
for s,p,o in g.triples((None,RDF.type,sbol_ns.ComponentDefinition)):
    cd_list.append(s)

display_list = []
for i in cd_list:
    display_list.append(g.value(i,sbol_ns.displayId))

parent_list = []
for i in cd_list:
    for s,p,o in g.triples((i,sbol_ns.component,None)):
        if o:
            parent_list.append(s)

parents = list(set(parent_list))

child_list = []
for i in parents:
    for s,p,o in g.triples((i,sbol_ns.component,None)):
         child_list.append(comp2compdef(o))

#Prints the displayId of the parent and child components
print 'Parents:'
for i in parents:
    print compdef2displayid(i)
print 'Children:'
for i in child_list:
    print compdef2displayid(i), comp2range(compdef2comp(i))