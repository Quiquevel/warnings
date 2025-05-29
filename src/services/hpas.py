import shuttlelib.db.mongo as mongolib
import os
from shuttlelib.utils.logger import logger
from src.services.devops import get_data_from_knowledge
from src.services.outputdict import set_output_base_dict


mg = mongolib.MongoClient()
mongocollection = os.getenv("COLLECTION_HPAS")
mg.change_collection(collection=mongocollection)

async def check_min_man(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Check if the minReplicas and maxReplicas of the HPA are equal, which indicates that the HPA is not scaling.'''
    if entity_id == None:
        entity_id = "spain"

    query = [{}]

    if cluster != None:
        query.append({"cluster": cluster})

    if region != None:
        query.append({"region": region})

    if namespace != None:
        query.append({"namespace": namespace})
    logger.info(f"Checking HPA minReplicas and maxReplicas for entity_id: {entity_id}, functional_environment: {functional_environment}, cluster: {cluster}, region: {region}, namespace: {namespace}, destination: {destination}")
    
    #Sometimes the HPA min replicas = max replicas = 1 when is the hidden block, depending on what leveling tool was used.
    query.append({"minReplicas": {"$gt": 1}})

    fullquery = {"$and": query}

    mongodata = mg.find(fullquery)
    logger.info(f"Querying MongoDB with: {fullquery}")
    
    outputlist = []
    

    for data in mongodata:
        logger.info(f"Checking HPA {data['name']} in namespace {data['namespace']} for minReplicas and maxReplicas.")
        min_replicas = data["minReplicas"]

        max_replicas = data["maxReplicas"]

        outputdict = {}

        if min_replicas == max_replicas:
            logger.info(f"HPA {data['name']} in namespace {data['namespace']} has minReplicas = maxReplicas = {min_replicas}.")
            outputdict = await set_output_base_dict(data,destination)
            outputdict.update({"min_replicas": min_replicas})
            outputdict.update({"max_replicas": max_replicas})
            
            outputlist.append(outputdict)

    return outputlist

async def check_unable_condition(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Check if the HPA has the condition "AbleToScale" set to False, which indicates that the HPA is unable to scale.'''
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
    logger.info(f"Querying MongoDB with: {fullquery}")
    mongodata = mg.find(fullquery)
    
    outputlist = []
    

    for data in mongodata:
        logger.info(f"Checking HPA {data['name']} in namespace {data['namespace']} for unable to scale condition.")
        try:
            abletoscale = data["ableToScale"]
        except KeyError:
            abletoscale = None

        outputdict = {}

        if abletoscale == "False":
            logger.info(f"HPA {data['name']} in namespace {data['namespace']} is unable to scale.")
            outputdict = await set_output_base_dict(data,destination)

            hpadata = {
                "hpaname": data["name"],
                "scaleTargetKind": data["scaleTargetKind"],
                "scaleTargetName": data["scaleTargetName"],
                "scaleTargetApiVersion": data["scaleTargetApiVersion"]
            }

            outputdict.update({"hpadata": hpadata})

            message = "unknown"
            for condition in data["hpaconditions"]:
                if condition["type"] == "AbleToScale":
                    message = condition["message"]
            
            abletoscale_msg = f'Unable to scale. Reason: {message}'

            outputdict.update({"abletoscale": abletoscale_msg})
            outputlist.append(outputdict)

    return outputlist
