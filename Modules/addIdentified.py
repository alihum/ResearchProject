from rdflib import URIRef, Graph, Literal
from rdflib.namespace import RDF

from inputfile import input_file
from namespaces import *

g = Graph()
g.parse(input_file)


def triple(s,p,o): # shortens adding triples
    g.add((s,p,o))


def identified_from_input():
    identified_list = ['uri','rdftype','persistentIdentity','displayId','version','wasDerivedFrom','name','description']

    identified_dct = dict.fromkeys(identified_list,None)

    for i in identified_list:
        identified_dct[i] = raw_input("What is the object {}?:".format(i)) or None

    return identified_dct


# Function to add an identified object (currently has dependencies on Namespace etc.)
def add_identified(uri,rdftype,persistentIdentity=None,displayId=None,version=None,wasDerivedFrom=None,name=None,description=None):
    triple(URIRef(uri), RDF.type, sbol_ns[rdftype])
    if persistentIdentity:
        triple(URIRef(uri), sbol_ns.persistentIdentity, URIRef(persistentIdentity))
    if displayId:
        triple(URIRef(uri), sbol_ns.displayId, URIRef(displayId))
    if version:
        triple(URIRef(uri), sbol_ns.version, Literal(version))
    if wasDerivedFrom:
        triple(URIRef(uri), prov.wasDerivedFrom, URIRef(wasDerivedFrom))
    if name:
        triple(URIRef(uri), dcterms.title, Literal(name))
    if description:
        triple(URIRef(uri), dcterms.description, Literal(description))

# Below here is an example of adding an identified object
default_dct = {'uri':"http://partsregistry.org/BBa_33345",  # URI for Component Definition (required)
               'rdftype':'ComponentDefinition',  # RDF type (required)
               'persistentIdentity':None,  # URI(s) to other versions (should use semantic versioning)
               'displayId':None,  # String for the display ID (composed of only alphanumberic or underscore characters
                                  # must not begin with a digit)
               'version':1,  # string to describe version number (compares two objects with the same persistentIdentity)
               'wasDerivedFrom':'http://partsregistry.com/cd/sequence',  # URI to SBOL or non-SBOL resource
               'name':'Hello',  # string displayed to human when vizualising an Identified object
               'description':None}  # more thorough text description of identified object

add_identified(**default_dct)

g.serialize('TestOutput.xml')