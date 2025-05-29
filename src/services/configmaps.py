import shuttlelib.db.mongo as mongolib
import os
from shuttlelib.utils.logger import logger
from src.services.devops import get_data_from_knowledge

mg = mongolib.MongoClient()


async def get_wrong_routing_dns_configmaps(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None):
    mongocollection = os.getenv("COLLECTION_CONFIGMAPS")
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

    configmap_objects = mg.find(fullquery)

    outputlist = []
    
    for micro in configmap_objects:
        logger.info(f'configmap object {micro}')
        name = micro["name"]        
        namespace = micro["namespace"]
        logger.info(f'namespace {namespace}')
        cluster = micro["cluster"]
        region = micro["region"]
        
        wrongroutingpaths = []

        for file in micro["pathslist"]:
            logger.info(f'file {file}')
            wrongroutingpaths = []     
            logger.info(f'configmap file {file["file"]}')
            if not any(ocustring in file["file"] for ocustring in ocustringslist):
                for path in file["pathslist"]:
                    logger.info(f'path {path}')
                    outputdict = {}
                    logger.info(f'path {path}')
                    variable = path["variable"]
                    value = path["value"]

                    if any(pattern in value for pattern in patternslist):
                        if not variable.startswith("#") and not any(element.lower() in str(variable).lower() for element in false_positive_variables_list) and not any(element in str(value).lower() for element in false_positive_values_list) and not value.endswith("html"):    
                            wrongroutingpaths.append(path)

            if wrongroutingpaths != []:
                namespaceinfo = await get_data_from_knowledge(namespace[:-4])
                devopslist = []
                try:
                    for devops in namespaceinfo[0]["devops"]:
                        logger.info(f'Adding devops {devops["name"]} to the list')
                        devopslist.append(devops["name"])
                except Exception as e:
                    logger.error(f'ERROR getting devops of namespace {namespace}: {e} ')

                outputdict = {
                    "devops": ",".join(devopslist),
                    "cluster": cluster,
                    "region": region,
                    "namespace": namespace,
                    "configuration object": name + " configmap",
                    "file": file["file"],
                    "wrongRouting": wrongroutingpaths
                }
                outputlist.append(outputdict)
                logger.info(f'Adding outputdict {outputdict} to the outputlist')
    return outputlist