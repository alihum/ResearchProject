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
    g.bind('example','http://example.com/')


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


def add_physicalcomponent(uri, rdftype, persistentIdentity=None,displayId=None,version=None,wasDerivedFrom=None,name=None, \
                description=None, definition=None, types=None, physicalLocation = None, invivo=None, invitro=None, experimentaldata=None):
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
    triple(URIRef(uri), RDF.type, sbol_ns[rdftype])
    if persistentIdentity:
        triple(URIRef(uri), sbol_ns.persistentIdentity, URIRef(persistentIdentity))
    if displayId:
        triple(URIRef(uri), sbol_ns.displayId, Literal(displayId))
    if version:
        triple(URIRef(uri), sbol_ns.version, Literal(version))
    if wasDerivedFrom:
        triple(URIRef(uri), prov.wasDerivedFrom, URIRef(wasDerivedFrom))
    if name:
        triple(URIRef(uri), dcterms.title, Literal(name))
    if description:
        triple(URIRef(uri), dcterms.description, Literal(description))
    if definition:
        triple(URIRef(uri),sbol_ns.definition,URIRef(uri))
    if types:
        for i in types:
            triple(URIRef(uri), example.types, URIRef(i))
    if physicalLocation:
        add_physicalLocation(**physicalLocation)
    if invivo:
        add_invivo(**invivo)
    if invitro:
        add_invitro(**invitro)
    if experimentaldata:
        for i in experimentaldata:
            add_experimentaldata(**i)


def add_physicalLocation(uri,lab=None,room=None,reference=None,temp=None):
    triple(URIRef(uri),RDF.type,example.physicalLocation)
    if lab:
        triple(URIRef(uri),example.lab,URIRef(lab))
    if room:
        triple(URIRef(uri),example.room,URIRef(room))
    if reference:
        triple(URIRef(uri),example.reference,URIRef(reference))
    if temp:
        triple(URIRef(uri),example.temperature,Literal(temp))

def add_invivo(uri,strainID,medium):
    triple(URIRef(uri),RDF.type,example.invivo)
    if strainID:
        triple(URIRef(uri),example.strain,URIRef(strainID))
    if medium:
        triple(URIRef(uri),example.medium,URIRef(medium))

def add_invitro(uri,container):
    triple(URIRef(uri),RDF.type,example.invitro)
    if container:
        triple(URIRef(uri),example.container,URIRef(container))

def add_experimentaldata(uri,type,attachment):
    triple(URIRef(uri),RDF.type,example.experimentaldata)
    if type:
        triple(URIRef(uri),example.type,URIRef(type))
    if attachment:
        triple(URIRef(uri),example.attachment,URIRef(attachment))

def add_physcial_component(input_file,physical_component_dct,output_file):
    """
    takes an activity dictionary and produces the activity object, associations and usages and saves to a file
    :param input_file: input file for adding to
    :param activity_dct: activity dictionary in normal format
    :param output_file: saves the output in specified file
    :return: 
    """
    parse_xml(input_file)
    add_physicalcomponent(**physical_component_dct)
    g.serialize(output_file,"xml")

physical_component_dct = {'uri':"http://example.com/physical/physicalcomponent1", #URI for Component Definition (required)
                'rdftype':'PhysicalComponent', #RDF type (required)
                'persistentIdentity':None, #URI(s) to other versions (should use semantic versioning)
                'displayId':'DNA synthesis', #String for the display ID (composed of only alphanumberic or underscore characters must not begin with a digit)
                'version':None, #string to describe version number (compares two objects with the same persistentIdentity)
                'wasDerivedFrom':None, #URI to SBOL or non-SBOL resource
                'name':'DNA synthesis', # string displayed to human when vizualising an Identified object
                'description':'DNA synthesis by DNA2.0',#more thorough text descrption of identified object}
                'definition':'http://synbiohub.org/public/igem/BBa_P0440/1',
                'types': [
                    'http://www.biopax.org/release/biopax-level3.owl#DnaRegion',   # agent in format
                    'http://identifiers.org/so/SO:0000987'  # (URI(req),hadRole(req),hadPlan)
                          ]
                ,

                'physicalLocation':{
                    'uri':'http://example.com/locations/location1',   # need to decide how to store locations properly
                    'lab':'http://example.com/labs/ICOS2',
                    'room':'http://example.com/labs/rooms/room3',
                            },

                'invivo':{
                    'uri':'http://example.com/invivo/invivo1',
                    'strainID':'http://purl.obolibrary.org/obo/NCBITaxon_224308', # use NCBI taxon classification
                    'medium':'http://example.com/invivo/media/lbbroth'
                          }
                          ,


                'invitro': {
                    'uri': 'http://example.com/invitro/invitro1',
                    'container' :'http://example.com/invitro/containers/eppendorf-tube'
                }
                          ,
                'experimentaldata': [

                    {
                        'uri': 'http://example.com/experimentaldata/experimentaldata1',
                        'type': 'http://example.com/experimentaldata/types/gelelectrophoresis',
                        'attachment': 'http://www.images.com/gelelectrophoresis.jpg'
                    }
                    ,
                    {
                        'uri': 'http://example.com/experimentaldata/experimentaldata2',
                        'type': 'http://example.com/experimentaldata/types/nanodrop',
                        'attachment': 'http://www.images.com/nanodrop-results.txt'
                    }

                ]
                }


add_physcial_component('BBa_P0440.xml',physical_component_dct,'BBa_P0440(physicaloutput).xml')