from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF
from namespaces import *
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
    g.bind("obo","http://purl.obolibrary.org/obo/")

# Function shortens adding triples by abbreviating g.add
def triple(s,p,o):
    '''
    Takes three arguments and adds them as an RDF truple
    :param s: subject of triple
    :param p: predicate of triple
    :param o: object of triple
    :return:
    '''
    g.add((s,p,o))

def addPhysicalContext(uri,type,name=None,barcode=None,contains=None,components=None,strainId=None):
    triple(URIRef(uri),RDF.type,URIRef("http://example.com/PhysicalContext"))
    triple(URIRef(uri),pc.type,URIRef(type))
    if name:
        triple(URIRef(uri),dcterms.title,Literal(name))
    if barcode:
        triple(URIRef(uri),obo.FLU_0001019,Literal(barcode))
    if contains:
        for i in contains:
            triple(URIRef(uri),pc.contains,URIRef(i["uri"]))
            addPhysicalContext(**i)
    if components:
        for i in components:
            triple(URIRef(uri),pc.components,URIRef(i))
    if strainId:
        triple(URIRef(uri),obo.OGG_0000000007,URIRef(strainId))


cellculture = {
    "uri":"http://example.com/room1/refrigeratorA/plate1/cellculture1",
    "type":"http://purl.obolibrary.org/obo/OBI_0001876",
    "strainId":"http://purl.obolibrary.org/obo/NCBITaxon_224308",
    "components":["http://example.com/physicalcomponents/physicalcomponent1"]
}

eppendorf = {
    "uri":"http://example.com/physicalcontext/room1/refrigeratorA/eppendorf1",
    "name":"16/07/17: Sample A"
    "type":"http://purl.obolibrary.org/obo/OBI_0000836",
    "components":["http://example.com/physicalcomponents/physicalcomponent3"]
}

plate = {
    "uri":"http://example.com/room1/refrigeratorA/plate1",
    "name":"Plate A",
    "type":"http://www.bioasssayontology.org/bao#BAO_0000513",
    "barcode":"12332324",
    "contains":[cellculture]
         }

fridge={
    "uri":"http://example.com/physicalcontext/room1/refrigeratorA",
    "type":"http://purl.obolibrary.org/obo/ENVO_01000583",
    "name":"Fridge A",
    "contains":[plate,eppendorf]

}

room = {
    "uri" : "http://example.com/phyiscalcontext/room1",
    "type" : "http://purl.obolibrary.org/obo/ENVO_00000073",
    "name":"RIDFB2.1.63",
    "contains":[fridge]
}

def fullPhysicalContext(input_file,physical_context_dct,output_file):
    parse_xml(input_file)
    addPhysicalContext(**physical_context_dct)
    g.serialize(output_file,"xml")

fullPhysicalContext("ComponentDefinitionOutput.rdf",room,"Output.xml")