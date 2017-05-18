from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF, FOAF
from statistics import mode

input_file = "/Users/ali/PycharmProjects/ResearchProject/Test01/TestInput.xml"
g = Graph()
g.parse(input_file)

sbol_ns = Namespace("http://sbols.org/v2#")
myapp = Namespace("http://myapp.com/")
prov = Namespace("http://www.w3.org/ns/prov#")
dcterms = Namespace("http://purl.org/dc/terms/")

#Finds the parent component definition (won't work for more than one layer of hierarchy)
lst = []
for s,p,o in g.triples((None,sbol_ns.component,None)):
    lst.append(s)

parent_definition = mode(lst)

#Finds child definitions of parent definition
child_definitions = []
for s,p,o in g.triples((parent_definition,sbol_ns.component,None)):
    child_definitions.append(o)


g.bind('myapp',myapp)

#A function that finds the predicates for Component Definitions
def ComponentDefinitionList(xml):
    x = []
    g = Graph()
    g.parse(xml)
    for s,p,o in g.triples((None,RDF.type,sbol_ns.ComponentDefinition)):
        x.append(s)
    return(x)

amdct = {'1':'BioBrick',
         '2':'BASIC',
         '3':'Gibson'}

amchoice = raw_input("Which assembly method?\n"+str(amdct))


#g.add((prov.Activity,RDF.about,myapp.biobrickassembly)) don't need both
bba = myapp['assembly/1']

g.add((bba,RDF.type,prov.Activity))
g.add((bba,prov.wasAssociatedWith,myapp['labs/ICOS']))
g.add((bba,dcterms.title,Literal(amchoice)))
g.add((bba,myapp.assemblytype,myapp[amdct[amchoice]]))


g.add((URIRef(parent_definition),prov.wasGeneratedBy,bba))
for i in child_definitions:
    g.add((URIRef(parent_definition),prov.wasDerivedFrom,URIRef(i)))


g.add((myapp['labs/ICOS'],RDF.type,prov.Agent))
g.add((myapp['labs/ICOS'],RDF.type,prov.Organsation))

# g.add((myapp['labs/ICOS']))

g.add((myapp['user001'],RDF.type,prov.Agent))
g.add((myapp['user001'],prov.actedOnBehalfOf,myapp['labs/ICOS']))

g.serialize("TestOutput.xml","xml")
#
# doc = Document()
#
# doc.read("TestOutput.xml")
#
# doc.write("SBOLOutput.xml")