from rdflib import Namespace, Graph
from rdflib.namespace import RDF

from inputfile import input_file
from read_sbol import comp2compdef

sbol_ns = Namespace("http://sbols.org/v2#")
myapp = Namespace("http://myapp.com/")
prov = Namespace("http://www.w3.org/ns/prov#")
dcterms = Namespace("http://purl.org/dc/terms/")

class SBOL:
    def __init__(self,input_file):
        self.g = Graph()
        self.g.parse(input_file)

    def ComponentDefinitionList(self):
        cd_list = []
        for s, p, o in self.g.triples((None, RDF.type, sbol_ns.ComponentDefinition)):
            cd_list.append(s)
        return cd_list


    def DisplayIdList(self):
        display_list = []
        for i in self.ComponentDefinitionList():
            display_list.append(self.g.value(i, sbol_ns.displayId))
        return display_list

    def ParentList(self):
        parent_list=[]
        for i in self.ComponentDefinitionList():
            for s, p, o in self.g.triples((i, sbol_ns.component, None)):
                if o:
                    parent_list.append(s)
        return list(set(parent_list))

    def ChildList(self):
        child_list = []
        for i in self.ParentList():
            for s,p,o in self.g.triples((i,sbol_ns.component,None)):
                 child_list.append(comp2compdef(o))
        return child_list


x = SBOL(input_file)

print 'Parents:'
for i in x.ParentList():
    print i

print 'Children:'
for i in x.ChildList():
    print i

# Sorts the parts into order and shows their start and end locations
# cdandrange = []
# for i in x.ChildList():
#     cdandrange.append((i,comp2start(compdef2comp(i)),comp2end(compdef2comp(i))))
#
#
# cdandrange.sort(key=lambda tup:tup[1])
#
# for i in cdandrange:
#     print i[0], i[1], i[2]