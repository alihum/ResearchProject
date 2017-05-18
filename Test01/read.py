from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF, FOAF
from statistics import mode
from inputfile import input_file

g = Graph()
g.parse(input_file)

sbol_ns = Namespace("http://sbols.org/v2#")
myapp = Namespace("http://myapp.com/")
prov = Namespace("http://www.w3.org/ns/prov#")
dcterms = Namespace("http://purl.org/dc/terms/")

# for s,p,o in g.triples((None,prov.wasDerivedFrom,None)):
#     print s, 'was derived from', o
#
# for s,p,o in g.triples((None,myapp.assemblytype,None)):
#     print o
#
# for s,p,o in g.triples((None,myapp.assemblytype,None)):


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