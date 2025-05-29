import shuttlelib.db.mongo as mongolib
import os
from shuttlelib.utils.logger import logger
from src.services.outputdict import set_output_base_dict

mg = mongolib.MongoClient()

async def get_production_block(namespaceid):
    '''Get the production block for a given namespace ID.'''
    mg.change_collection(collection=os.getenv("COLLECTION"))
    namespace = mg.find_one({"namespaceid": namespaceid})
    try:
        production_block = namespace["productionBlock"]
        logger.info(f'Production block for namespace {namespaceid}: {production_block}')
    except KeyError:
        production_block = None
    return production_block

async def get_wrong_routing_dnss_configurationservice(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Get the wrong routing DNS for a given entity_id, functional_environment, cluster, region, namespace, and destination.'''
    mongocollection = os.getenv("COLLECTION")
    mg.change_collection(collection=mongocollection)

    patternslist = os.getenv('WRONGROUTING_PATTERNS').split(",")
    false_positive_variables_list = os.getenv("FALSE_POSITIVE_VARIABLES_LIST").split(",")
    false_positive_values_list = os.getenv("FALSE_POSITIVE_VALUES_LIST").split(",")
    ocustringslist = os.getenv("OCU_STRING_LIST").split(",")

    if entity_id == None:
        entity_id = "spain"

    query = [{}]

    if region != None:
        query.append({"region": region})

    if cluster != None:
        query.append({"cluster": cluster})

    if namespace != None:
        query.append({"namespace": namespace})

    query.append({"pathslist": {"$exists": True}})
    query.append({"pathslist": {"$not": {"$size": 0}}})

    fullquery = {"$and": query}
    logger.info(f'Querying MongoDB with: {fullquery}')

    namespaceobjects = mg.find(fullquery)


    outputlist = []
    
    for namespaceobj in namespaceobjects:
        wrongroutingpaths = []
        for configservice in namespaceobj["pathslist"]:
            logger.info(f'configservice {configservice["configservice"]}')
            for file in configservice["files"]:
                wrongroutingpaths = []
                logger.debug(f'file {file["file"]}')
                if not any(ocustring in file["file"] for ocustring in ocustringslist):
                    for path in file["pathslist"]:
                        logger.debug(f'path {path}')
                        variable = path["variable"]
                        value = path["value"]
                        if any(pattern in value for pattern in patternslist):
                            if not any(element.lower() in str(variable).lower() for element in false_positive_variables_list) and not any(element in str(value).lower() for element in false_positive_values_list) and not value.endswith("html"):    
                                wrongroutingpaths.append(path)

                if wrongroutingpaths != []:
                    outputdict = await set_output_base_dict(namespaceobj,destination)

                    outputdict.update({
                        "configuration object": configservice["configservice"],
                        "file": file["file"],
                        "wrongRouting": wrongroutingpaths
                    })

                    outputlist.append(outputdict)
    logger.info(f'outputlist {outputlist}')                      
    return outputlist