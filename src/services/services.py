import shuttlelib.db.mongo as mongolib
import os
from shuttlelib.utils.logger import logger
from datetime import datetime
from src.services.devops import get_data_from_knowledge, get_devops_list
from src.services.outputdict import set_output_base_dict

today = datetime.today()
today = datetime(year=today.year,month=today.month,day=today.day)

mg = mongolib.MongoClient()

async def get_routing_services(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):   
    '''Get the microservices that have routing status KO, meaning they are not routing traffic correctly.'''
    mongocollection = os.getenv("COLLECTION")
    mg.change_collection(collection=mongocollection)
    exceptednamespaces = os.getenv("EXCEPTED_NAMESPACES_FOR_ROUTING_SERVICES").split(",")
    exceptedmicroservices = os.getenv("EXCEPTED_MICROS_FOR_ROUTING_SERVICES").split(",")

    ## NO SERVICE ROUTING TO THIS MICROSERVICE
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
    logger.info(f"Querying MongoDB with: {fullquery}")
    
    outputlist = []

    routing_ko_list = []
    for data in mongodata:
        logger.info('Processing data from MongoDB')
        if data["evaluation"]["routingStatus"] == "KO":
            routing_ko_list.append(data["namespaceid"])

    noserviceslist = os.getenv("NO_SERVICES_MICROS").split(",")
    if routing_ko_list != []:
        mongocollection = os.getenv("COLLECTION_MICROSERVICES")
        mg.change_collection(collection=mongocollection)

        for namespaceid in routing_ko_list:
            logger.info('Processing namespaceid for routing KO')
            if any(ns in namespaceid for ns in exceptednamespaces) or any(cluster in namespaceid for cluster in ["confluent","probks","dmzbbks"]):
                continue

            mongodata = mg.find({"namespaceid": namespaceid})
            microservicelist = []
            for micro in mongodata:
                logger.info('Processing microservice in namespace')
                if micro["name"] not in noserviceslist and micro["micro_status"]["reason"] == "No services routing to this microservice" and not any(microservice in micro["name"] for microservice in exceptedmicroservices):
                    #double check if micro's name contains noserviceslist name:
                    if not any(noserviceselem in micro["name"] for noserviceselem in noserviceslist):
                        microservicelist.append(micro["kind"]+"-"+micro["name"])
            
            if microservicelist != []:
                logger.info(f'Found microservices with routing KO in namespaceid {namespaceid}: {microservicelist}')
                cluster = namespaceid[:namespaceid.find("-")]
                nocluster = namespaceid[namespaceid.find("-")+1:]
                region = nocluster[:nocluster.find("-")]
                namespace = namespaceid[len(cluster)+1+len(region)+1:]

                microservicestr = ','.join(microservicelist)

                #Not setting outputdict like in other codes because of the way the data is looped here (not getting info directly from mongo)
                namespaceinfo = await get_data_from_knowledge(namespace[:-4])
                logger.info(f'Getting info of namespace {namespace}')
                devopslist = await get_devops_list(namespaceinfo,namespace,destination)

                outputdict = {
                    "devops": ",".join(devopslist),
                    "cluster": cluster,
                    "region": region,
                    "namespace": namespace,
                    "microservices": microservicestr
                }

                outputlist.append(outputdict)
    logger.info("Output list for routing services returned")
    return outputlist

async def get_services_routing_nowhere(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Get the services that are routing nowhere, meaning they have a selector status of KO and no microservice is associated with them.'''
    exceptednamespaces = os.getenv("EXCEPTED_NAMESPACES_FOR_SERVICES_ROUTING_NOWHERE").split(",")

    mongocollection = os.getenv("COLLECTION_SERVICES")
    mg.change_collection(collection=mongocollection)

    ## SERVICES ROUTING TO NOWHERE. THERE IS NO MICRO DESTINATION WELL MATCHING THE SELECTOR LABEL
    if entity_id == None:
        entity_id = "spain"

    query = [{}]

    if cluster != None:
        query.append({"cluster": cluster})

    if region != None:
        query.append({"region": region})

    if namespace != None:
        query.append({"namespace": namespace})        

    query.append({"selector_status.status": "KO"})

    fullquery = {"$and": query}

    mongodata = mg.find(fullquery)
    logger.info(f"Constructed query: {fullquery}")
    
    outputlist = []

    for data in mongodata:
        logger.info('Processing data from MongoDB')
        cluster = data["cluster"]
        region = data["region"]
        namespace = data["namespace"]
        service = data["name"]
        creationdate = data["creationTimestamp"]
        selectors = data["selectors"]

        if namespace in exceptednamespaces and cluster == "confluent": #sanes-adn360 de confluent usa vostok para desplegar y necesita servicios aunque no haya micro asociado
            continue

        try:
            logger.info('Processing service in namespace')
            creationdate_datetime = datetime.strptime(creationdate,"%Y-%m-%dT%H:%M:%SZ")
            dates_difference = today - creationdate_datetime
            days = dates_difference.days
        except Exception as e:
            logger.error(f'There was an error with date operations: {e}')
            days = 365

        days_for_reporting = int(os.getenv("DAYS_FOR_REPORTING"))
        if days < days_for_reporting: #If service has no microservice for routing to but it was created less than {DAYS_FOR_START_REPORTING} days ago it will not be shown in the report
            continue        

        outputdict = await set_output_base_dict(data,destination)

        outputdict.update({
            "service": service,
            "selectors": selectors
        })

        outputlist.append(outputdict)
    logger.info("Output list for services routing nowhere returned")
    return outputlist