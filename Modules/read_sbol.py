from rdflib import URIRef, Namespace, Graph
from rdflib.namespace import RDF
from namespaces import *

def parse_xml(input_file):
    """
    Parses input file to graph object
    :param input_file: input file as .xml
    :return: 
    """
    global g
    g = Graph()
    g.parse(input_file)

def comp2compdef(component):
    for s, p, o in g.triples((URIRef(component),sbol_ns.definition,None)):
        return(o)

# print ComponentDefinitionFromComponent("http://partsregistry.org/cd/BBa_F2620/luxR",input_file)

def compdef2comp(component_def):
    for s, p, o in g.triples((None, sbol_ns.definition, URIRef(component_def))):
        return s

# print ComponentFromComponentDefinition("http://partsregistry.org/cd/BBa_B0034",input_file)

def comp2partseq(component):
    for s, p, o in g.triples((URIRef(component),sbol_ns.definition,None)):
        cd = o
    for s, p, o in g.triples((URIRef(cd),sbol_ns.sequence,None)):
        seq = o
    for s, p, o in g.triples((URIRef(seq),sbol_ns.elements,None)):
        return(o)

# print PartSequenceFromComponent("http://partsregistry.org/cd/BBa_F2620/rbs",input_file)

def compdef2displayid(componentdefinition):
    for s,p,o in g.triples((componentdefinition,sbol_ns.displayId,None)):
        return o

def comp2range(component):
    for s,p,o in g.triples((None,sbol_ns.component,component)):
        sa = s
        for s,p,o in g.triples((sa,sbol_ns.location,None)):
             x = o
             for s,p,o in g.triples((x,sbol_ns.start,None)):
                start = o
             for s,p,o in g.triples((x,sbol_ns.end,None)):
                end = o
    return start, end

def comp2start(component):
    for s,p,o in g.triples((None,sbol_ns.component,component)):
        sa = s
        for s,p,o in g.triples((sa,sbol_ns.location,None)):
             x = o
             for s,p,o in g.triples((x,sbol_ns.start,None)):
                start = o
             return start

def comp2end(component):
    for s,p,o in g.triples((None,sbol_ns.component,component)):
        sa = s
        for s,p,o in g.triples((sa,sbol_ns.location,None)):
             x = o
             for s,p,o in g.triples((x,sbol_ns.end,None)):
                end = o
             return end




# print ComponentToRange(URIRef('http://partsregistry.org/cd/BBa_F2620/luxR'),input_file)

class SBOL:
    def __init__(self,input_file):
        self.g = Graph()
        self.g.parse(input_file)
        parse_xml(input_file)

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

x = SBOL("BBa_P0440.xml")

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