from rdflib import URIRef, Namespace, Graph, Literal
from rdflib.namespace import RDF, FOAF
from inputfile import input_file

g = Graph()
g.parse(input_file)

def triple(x,y,z):
    g.add((x,y,z))

sbol_ns = Namespace("http://sbols.org/v2#")
myapp = Namespace("http://myapp.com/")
prov = Namespace("http://www.w3.org/ns/prov#")
dcterms = Namespace("http://purl.org/dc/terms/")

default_dct = {'uri':"http://partsregistry.org/BBa_33345", #URI for Component Definition (required)
            'rdftype':'ComponentDefinition', #RDF type (required)
            'persistentIdentity':None, #URI(s) to other versions (should use semantic versioning)
            'displayId':None, #String for the display ID (composed of only alphanumberic or underscore characters must not begin with a digit)
            'version':1, #string to describe version number (compares two objects with the same persistentIdentity)
            'wasDerivedFrom':'http://partsregistry.com/cd/sequence', #URI to SBOL or non-SBOL resource
            'name':'Hello', # string displayed to human when vizualising an Identified object
            'description':None} #more thorough text descrption of identified object

component_defintion = {'types':['http://www.biopax.org/release/biopax- level3.owl#DnaRegion','http://identifiers.org/so/SO:0000987'],
                       'roles':['http://identifiers.org/so/SO:0000167'],
                       'sequences':[],
                       'components':[]}

def IdentifiedDictionaryFromInput():
    identified_list = ['uri','rdftype','persistentIdentity','displayId','version','wasDerivedFrom','title','description']

    identified_dct = dict.fromkeys(identified_list,None)

    for i in identified_list:
        identified_dct[i] = raw_input("What is the object {}?:".format(i)) or None

    return identified_dct

def AddComponentDefinition(identified_dct,types,roles,sequences,components):
    AddIdentified(**identified_dct)
    cduri = identified_dct['uri']
    for i in types:
        g.add((URIRef(cduri),sbol_ns.type,URIRef(i)))
    if roles:
        for i in roles:
            g.add((URIRef(cduri),sbol_ns.role,URIRef(i)))
    if sequences:
        for i in sequences:
            g.add((URIRef(cduri),sbol_ns.sequence,URIRef(i)))
    if components:
        for i in components:
            g,add((URIRef(cduri),sbol_ns.component,URIRef(i)))



# Function to add an identified object (currently has dependencies on Namespace etc.)
def AddIdentified(uri,rdftype,persistentIdentity=None,displayId=None,version=None,wasDerivedFrom=None,name=None,description=None):
    if rdftype == 'ComponentDefintion':
        g.add((URIRef(uri), RDF.type, sbol_ns[rdftype]))
    elif rdftype == 'Activity':
        g.add ==((URIRef(uri), RDF.type, prov.Activity))
    if persistentIdentity:
        g.add((URIRef(uri), sbol_ns.persistentIdentity, URIRef(persistentIdentity)))
    if displayId:
        g.add((URIRef(uri), sbol_ns.displayId, URIRef(displayId)))
    if version:
        g.add((URIRef(uri), sbol_ns.version, Literal(version)))
    if wasDerivedFrom:
        g.add((URIRef(uri), prov.wasDerivedFrom, URIRef(wasDerivedFrom)))
    if name:
        g.add((URIRef(uri), dcterms.title, Literal(name)))
    if description:
        g.add((URIRef(uri), dcterms.description, Literal(description)))

dnasynthesisactivity_dct = {'uri':"http://partsregistry.org/activites/activity1", #URI for Component Definition (required)
                'rdftype':'Activity', #RDF type (required)
                'persistentIdentity':None, #URI(s) to other versions (should use semantic versioning)
                'displayId':None, #String for the display ID (composed of only alphanumberic or underscore characters must not begin with a digit)
                'version':None, #string to describe version number (compares two objects with the same persistentIdentity)
                'wasDerivedFrom':None, #URI to SBOL or non-SBOL resource
                'name':'DNA synthesis', # string displayed to human when vizualising an Identified object
                'description':'DNA synthesis by DNA2.0',#more thorough text descrption of identified object}
                'agents':['http://example.com/agents/user001','http://example.com/agents/organisations/DNA2.0'],
                'entities':['http://partsregistry.org/cd/BBa_R0040']}

def AddActivity(uri,rdftype,persistentIdentity=None,displayId=None,version=None,wasDerivedFrom=None,name=None, \
                description=None,agents=None, entities = None):
    g.add ==((URIRef(uri), RDF.type, prov.rdftype))
    if persistentIdentity:
        g.add((URIRef(uri), sbol_ns.persistentIdentity, URIRef(persistentIdentity)))
    if displayId:
        g.add((URIRef(uri), sbol_ns.displayId, URIRef(displayId)))
    if version:
        g.add((URIRef(uri), sbol_ns.version, Literal(version)))
    if wasDerivedFrom:
        g.add((URIRef(uri), prov.wasDerivedFrom, URIRef(wasDerivedFrom)))
    if name:
        g.add((URIRef(uri), dcterms.title, Literal(name)))
    if description:
        g.add((URIRef(uri), dcterms.description, Literal(description)))
    if agents:
        for i in agents:
            g.add((URIRef(uri), prov.wasAssociatedWith, URIRef(i)))
        for i in agents:
            g.add((URIRef(i),RDF.type,prov.Agent))
    if entities:
        for i in entities:
            g.add((URIRef(i), prov.wasGeneratedBy, URIRef(uri)))

qualified_association_dct = {'activity':'http://partsregistry.org/activites/activity1',
                             'uri':'http://partsregistry.org/cd/BBa_F2620/association1',
                             'hadPlan':'http://www.example.com/genbankfile',
                             'hadRole':'http://www.example.com/DNAsynthesis',
                             'agent':'http://example.com/agents/user001'}


def add_qualified_association(activity,uri,hadPlan=None,hadRole=None,agent=None): #had to include activity as it
                                                                        #tell the association who its parent is
    g.add((URIRef(activity),prov.qualifiedAssociation,URIRef(uri)))
    g.add((URIRef(uri),RDF.type,prov.Association))
    if hadPlan:
        for i in hadPlan:
            g.add((URIRef(uri),prov.hadPlan,URIRef(hadPlan)))
    if hadRole:
        for i in hadRole:
            g.add((URIRef(uri),prov.hadRole,URIRef(hadRole)))
    if agent:
        for i in agent:
            g.add((URIRef(uri),prov.agent,URIRef(agent)))
#
# def add_qualified_usage(uri,entity,hadRole):
#     triple(URIRef(uri),RDF.type,prov)

#Test for adding component definition
# AddComponentDefinition(default_dct,**component_defintion)

AddActivity(**dnasynthesisactivity_dct)

add_qualified_association(**qualified_association_dct)

g.serialize("TestOutput3.xml","xml")