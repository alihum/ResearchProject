from rdflib import URIRef, Graph

from addIdentified import add_identified
from inputfile import input_file
from namespaces import *

g = Graph()
g.parse(input_file)


def triple(s,p,o): # shortens adding triples
    g.add((s,p,o))


def add_cd(identified_dct,types,roles,sequences,components):
    add_identified(**identified_dct)
    cduri = identified_dct['uri']
    for i in types:
        triple(URIRef(cduri),sbol_ns.type,URIRef(i))
    if roles:
        for i in roles:
            triple(URIRef(cduri),sbol_ns.role,URIRef(i))
    if sequences:
        for i in sequences:
            triple(URIRef(cduri),sbol_ns.sequence,URIRef(i))
    if components:
        for i in components:
            triple(URIRef(cduri),sbol_ns.component,URIRef(i))


default_dct = {'uri':"http://partsregistry.org/BBa_33345", #URI for Component Definition (required)
            'rdftype':'ComponentDefinition', #RDF type (required)
            'persistentIdentity':None, #URI(s) to other versions (should use semantic versioning)
            'displayId':None, #String for the display ID (composed of only alphanumberic or underscore characters must not begin with a digit)
            'version':1, #string to describe version number (compares two objects with the same persistentIdentity)
            'wasDerivedFrom':'http://partsregistry.com/cd/sequence', #URI to SBOL or non-SBOL resource
            'name':'Hello', # string displayed to human when vizualising an Identified object
            'description':None} #more thorough text descrption of identified object

component_definition = {'types':['http://www.biopax.org/release/biopax- level3.owl#DnaRegion','http://identifiers.org/so/SO:0000987'],
                       'roles':['http://identifiers.org/so/SO:0000167'],
                       'sequences':[],
                       'components':[]}

add_cd(default_dct,**component_definition)

g.serialize('TestOutput.xml')