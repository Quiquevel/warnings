import shuttlelib.db.mongo as mongolib
from shuttlelib.utils.logger import logger
import os
from src.services.outputdict import set_output_base_dict

mg = mongolib.MongoClient()
mongocollection = os.getenv("COLLECTION")
mg.change_collection(collection=mongocollection)

async def get_full_name(elem):
    '''Get the full name of the element based on its abbreviation.'''
    match elem:
        case "rc": 
            return "replicationControllers"
        case "dcs": 
            return "deploymentConfigs"
        case "cms": 
            return "configMaps"
        case "rs": 
            return "replicaSets"
        case "dss": 
            return "deployments"
        case _:
            return elem


async def get_quotas(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Get the quotas for a given entity_id, functional_environment, cluster, region, namespace, and destination.'''
    quota_warning_percentage = int(os.getenv("QUOTA_WARNING_PERCENTAGE"))
    quota_exceeded_percentage = int(os.getenv("QUOTA_EXCEEDED_PERCENTAGE"))

    if entity_id == None:
        entity_id = "spain"

    query = [{}]

    if cluster != None:
        query.append({"cluster": cluster})

    if region != None:
        query.append({"region": region})

    if namespace != None:
        query.append({"namespace": namespace})

    fullquery = {"$and": query}

    mongodata = mg.find(fullquery)
    logger.info(f'Querying MongoDB with: {fullquery}')
    
    outputlist = []

    objects_to_warn_str = os.getenv("OBJECTS_TO_WARN")
    objects_to_alert_str = os.getenv("OBJECTS_TO_ALERT")

    objects_to_warn = objects_to_warn_str.split(",")
    objects_to_alert = objects_to_alert_str.split(",")

    for data in mongodata:
        logger.info(f'Processing data: {data}')
        quotaexceededlist = []
        quotawarninglist = []
        for element, value in data["evaluation"].items():
            logger.info(f'Checking element {element} with value {value}')
            if "Quota" in element:
                if value != None:
                    if value >= quota_warning_percentage and value < quota_exceeded_percentage:
                        elem = await get_full_name(element[:-5])
                        if elem in objects_to_warn:
                            quotawarninglist.append(elem)
                    elif value >= quota_exceeded_percentage:
                        elem = await get_full_name(element[:-5])
                        if elem in objects_to_alert:
                            quotaexceededlist.append(elem)


        if quotaexceededlist != [] or quotawarninglist != []:
            
            outputdict = await set_output_base_dict(data,destination)                 

            outputdict.update({
                "quotawarning": ','.join(quotawarninglist),
                "quotaexceeded": ','.join(quotaexceededlist)
            })

            outputlist.append(outputdict)
    logger.info(f'Output list for quotas: {outputlist}')
    return outputlist