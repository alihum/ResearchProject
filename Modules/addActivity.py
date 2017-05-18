from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF
from namespaces import *

from inputfile import input_file

g = Graph()
g.parse(input_file)

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


def add_activity(uri,rdftype,persistentIdentity=None,displayId=None,version=None,wasDerivedFrom=None,name=None, \
                description=None,agents=None, entities = None):
    '''
    Takes an activity dictionary and adds the appropriate triples to the graph
    :param uri: Uniform Resource Identifier of the activity (required)
    :param rdftype: Should be Activity for an activity object (required)
    :param persistentIdentity: to refer to previous versions
    :param displayId: displayId in SBOL applications
    :param version: used to determine the difference between persistentIdentity's
    :param wasDerivedFrom: what it is derived from
    :param name: human-readble identifier
    :param description:  human-readable string to describe object
    :param agents: list of agents
    :param entities: list of entities
    :return: 
    '''
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


def add_qualified_association(activity, uri, agent, hadRole, hadPlan=None):
    """
    :param activity: parent activity of qualifiedAssociation (required)
    :param uri: Uniform Resource Identifier of association object (required)
    :param agent: the agent that was associated with the activity (required)
    :param hadRole: the role that the agent played (required)
    :param hadPlan: information that was used by the agent to implement the plan (URI)
    :return: 
    """
    triple(URIRef(activity),prov.qualifiedAssociation,URIRef(uri))
    triple(URIRef(uri),RDF.type,prov.Association)
    for i in agent:
        triple(URIRef(uri),prov.agent,URIRef(agent))
    for i in hadRole:
        triple(URIRef(uri), prov.hadRole, URIRef(hadRole))
    if hadPlan:
        for i in hadPlan:
            triple(URIRef(uri),prov.hadPlan,URIRef(hadPlan))


def add_qualified_usage(activity, uri, entity, hadRole):
    """
    :param activity: takes parent activity to refer to
    :param uri: uri of the qualified usage
    :param entity: uri of the entity used by the activity
    :param hadRole: role of the entity in the activity
    :return: 
    """
    triple(URIRef(activity), prov.qualifiedUsage, URIRef(uri))
    triple(URIRef(uri), RDF.type, prov.Usage)
    triple(URIRef(uri), prov.entity, URIRef(entity))
    triple(URIRef(uri), prov.hadRole, example[hadRole])


def qualified_association_from_activity(activity):
    """
    Takes an activity dictionary and automatically produces association objects
    :param activity: takes an activity dictionary
    :return: 
    """
    for i in range(len(activity['agents'])):
        add_qualified_association(activity['uri'],
                                  activity['uri']+'/association'+str(i+1),
                                  activity['agents'][i][0],
                                  activity['agents'][i][1],
                                  activity['agents'][i][2])


def qualified_usages_from_activity(activity):
    """
    Takes an activity dicitionary and automatically produces usage objects
    :param activity: activity dictionary
    :return: 
    """
    for i in range(len(activity['entities'])):
         add_qualified_usage(activity['uri'],
                            activity['uri']+'/usage'+str(i+1),  # uri needs substituting for base uri
                            activity['entities'][i][0],
                            activity['entities'][i][1])


def add_activity_full(activity_dct,output_file):
    """
    takes an activity dictionary and produces the activity object, associations and usages and saves to a file
    :param activity_dct: activity dictionary in normal format
    :param output_file: saves the output in specified file
    :return: 
    """
    add_activity(**activity_dct)
    qualified_association_from_activity(activity_dct)
    qualified_usages_from_activity(activity_dct)
    g.serialize(output_file,"xml")

dna_synthesis_activity = {'uri':"http://example.com/activities/dna-synthesis", #URI for Component Definition (required)
                'rdftype':'Activity', #RDF type (required)
                'persistentIdentity':None, #URI(s) to other versions (should use semantic versioning)
                'displayId':'DNA synthesis', #String for the display ID (composed of only alphanumberic or underscore characters must not begin with a digit)
                'version':None, #string to describe version number (compares two objects with the same persistentIdentity)
                'wasDerivedFrom':None, #URI to SBOL or non-SBOL resource
                'name':'DNA synthesis', # string displayed to human when vizualising an Identified object
                'description':'DNA synthesis by DNA2.0',#more thorough text descrption of identified object}

                'agents':[('http://example.com/agents/user001','http://example.com/roles/user','')   ,   # agent in format
                          ('http://example.com/agents/organisations/DNA2.0','http://example.com/roles/dna-synthesiser','')  # (URI(req),hadRole(req),hadPlan)
                          ]
                ,

                'entities':[("http://synbiohub.org/public/igem/BBa_M39017/1",'output'), # entity in format (URI,I/O)
                            ('http://parts.igem.org/Part:BBa_M39017','input')]}


add_activity_full(dna_synthesis_activity,"BBa_M39017(output).xml")