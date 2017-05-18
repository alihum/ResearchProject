from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF
from namespaces import *

from inputfile import input_file

g = Graph()
g.parse(input_file)



def triple(s,p,o): # shortens adding triples
    g.add((s,p,o))

def add_activity(uri,rdftype,persistentIdentity=None,displayId=None,version=None,wasDerivedFrom=None,name=None, \
                description=None,agents=None, entities = None):
    triple(URIRef(uri), RDF.type, prov[rdftype])
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
    if agents:
        for i in agents:
            triple(URIRef(uri), prov.wasAssociatedWith, URIRef(i))
        for i in agents:
            triple(URIRef(i),RDF.type,prov.Agent)
    if entities:
        for i in entities:
            triple(URIRef(i[0]), prov.wasGeneratedBy, URIRef(uri)) # 0 selects the URI from the URI,input/output) tuple
        for i in entities:
            triple(URIRef(uri),prov.used,URIRef(i[0]))


def add_qualified_association(activity,uri,agent=None,hadPlan=None,hadRole=None): #had to include activity as it
                                                                        #tell the association who its parent is
    triple(URIRef(activity),prov.qualifiedAssociation,URIRef(uri))
    triple(URIRef(uri),RDF.type,prov.Association)
    if hadPlan:
        for i in hadPlan:
            triple(URIRef(uri),prov.hadPlan,URIRef(hadPlan))
    if hadRole:
        for i in hadRole:
            triple(URIRef(uri),prov.hadRole,URIRef(hadRole))
    if agent:
        for i in agent:
            triple(URIRef(uri),prov.agent,URIRef(agent))


def add_qualified_usage(activity, uri, entity, hadRole):
    triple(URIRef(activity), prov.qualifiedUsage, URIRef(uri))
    triple(URIRef(uri), RDF.type, prov.Usage)
    triple(URIRef(uri), prov.entity, URIRef(entity))
    triple(URIRef(uri), prov.hadRole, myapp[hadRole])
    if hadRole == 'output':
        triple(URIRef(uri),prov.wasGeneratedBy,URIRef(activity))

activity_dct = {'uri':"http://partsregistry.org/activites/activity1", #URI for Component Definition (required)
                'rdftype':'Activity', #RDF type (required)
                'persistentIdentity':None, #URI(s) to other versions (should use semantic versioning)
                'displayId':None, #String for the display ID (composed of only alphanumberic or underscore characters must not begin with a digit)
                'version':None, #string to describe version number (compares two objects with the same persistentIdentity)
                'wasDerivedFrom':None, #URI to SBOL or non-SBOL resource
                'name':'DNA synthesis', # string displayed to human when vizualising an Identified object
                'description':'DNA synthesis by DNA2.0',#more thorough text descrption of identified object}

                'agents':[('http://example.com/agents/user001','','')   ,   # agent in format (URI,hadPlan,hadRole)
                          ('http://example.com/agents/organisations/DNA2.0','','')
                          ]
                ,

                'entities':[('http://partsregistry.org/cd/BBa_R0040','output'), # entity in format (URI,I/O)
                            ('http://parts.igem.org/Part:BBa_R0040','input')]}


qualified_association_dct = {'activity':'http://partsregistry.org/activites/activity1',
                             'uri':'http://partsregistry.org/cd/BBa_F2620/association1',
                             'hadPlan':'http://www.example.com/genbankfile',
                             'hadRole':'http://www.example.com/DNAsynthesis',
                             'agent':'http://example.com/agents/user001'}

def qualified_association_from_activity(activity):
    for i in range(len(activity['agents'])):
        add_qualified_association(activity['uri'],
                                  activity['uri']+'/association'+str(i+1),
                                  activity['agents'][i][0],
                                  activity['agents'][i][1],
                                  activity['agents'][i][2])


# need to put in addActivity module
def qualified_usages_from_activity(activity):
        for i in range(len(activity['entities'])):
            add_qualified_usage(activity['uri'],
                            activity['uri']+'/usage'+str(i+1),  # uri needs substituting for base uri
                            activity['entities'][i][0],
                            activity['entities'][i][1])


add_activity(**activity_dct)

qualified_association_from_activity(activity_dct)

qualified_usages_from_activity(activity_dct)

g.serialize("TestOutput.xml","xml")