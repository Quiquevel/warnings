import shuttlelib.db.mongo as mongolib
import os
from shuttlelib.utils.logger import logger
from src.services.outputdict import set_output_base_dict

mg = mongolib.MongoClient()
mongocollection = os.getenv("COLLECTION_MICROSERVICES")
mg.change_collection(collection=mongocollection)
exception_variables_list = os.getenv("EXCEPTION_VARIABLES_LIST").split(",")

async def ignore_consecutive_spaces(iterator, string):
    """
    Ignore consecutive spaces in a string starting from a given iterator position.

    Args:
        iterator (int): The starting position of the iterator.
        string (str): The input string.

    Returns:
        int: The updated iterator position after ignoring consecutive spaces.
    """
    i = iterator
    lenstring = len(string)
    while i < (lenstring-1) and string[i+1] == " ":
        i += 1
    return i

async def compare_diff_var(string1, string2):
    """
    Compare two strings character by character, ignoring leading and trailing spaces.
    
    Args:
        string1 (str): The first string to compare.
        string2 (str): The second string to compare.
    
    Returns:
        bool: False if the strings are equal after ignoring leading and trailing spaces, True otherwise.
    """

    if (string1 is None and string2 is not None) or (string1 is not None and string2 is None):
        return True

    i = 0
    j = 0
    different = False
    len1 = len(string1)
    len2 = len(string2)

    while i < len1 and j < len2:
        if string1[i] != string2[j]:
            different = True
            break
        elif string1[i] == " ":  # If it is a space, we need to skip all the spaces until the next character
             i = await ignore_consecutive_spaces(i, string1)
             j = await ignore_consecutive_spaces(j, string2)
             
        i += 1
        j += 1

    if i != len1 or j != len2:
        different = True

    return different

async def check_env_var(variablesmicro1,variablesmicro2):
    outputdict = {}
    different = False
    envvarstring1 = "initstring"
    envvarstring2 = "initstring"
    for key1,value1 in variablesmicro1.items():
        different_string = False
        try:
            value2 = variablesmicro2[key1]
            keyok = True
        except KeyError:
            keyok = False
            key2="null"
            value2 = "null"

        if keyok:
            key2=key1
            
            #To avoid getting difference but only for the region value of some variable:
            if value2 != None: 
                value2=value2.replace("bo2","bo1")
                value2 = value2.replace("weu2","weu1")
                value2=value2.replace("BO2","BO1")
                value2 = value2.replace("WEU2","WEU1")
                different_string = await compare_diff_var(value1, value2)
        
            
            if  different_string and key1 not in exception_variables_list:
                different = True
                envvarstring1 = f'{envvarstring1}, {key1}: {value1}'
                envvarstring2 = f'{envvarstring2}, {key2}: {value2}'
                
        else:
            different = True
            envvarstring1 = f'{envvarstring1}, {key1}: {value1}'
            envvarstring2 = f'{envvarstring2}, {key2}: {value2}'
        
        if different:
            envvarstring1 = envvarstring1.replace("initstring, ","")
            envvarstring2 = envvarstring2.replace("initstring, ","")
            outputdict.update({"bo1": envvarstring1, "bo2": envvarstring2})
    
    return outputdict
        
async def check_image(imagemicro1,imagemicro2):
    outputdict = {}
    
    differentimage = False
    for key1,value1 in imagemicro1.items():
        try:
            value2 = imagemicro2[key1]
            key_ok = True
        except KeyError:
            key_ok = False
            value2 = "null"

        if key_ok:
            if value1 != value2:
                differentimage = True
        else:
            differentimage = True
        
    if differentimage:
        if imagemicro1["registry"] == None:
            fullimagemicro1 = imagemicro1["project"]+"/"+imagemicro1["name"]+":"+imagemicro1["tag"]
        else:            
            fullimagemicro1 = imagemicro1["registry"]+"/"+imagemicro1["project"]+"/"+imagemicro1["name"]+":"+imagemicro1["tag"]

        if imagemicro2["registry"] == None:
            fullimagemicro2 = imagemicro2["project"]+"/"+imagemicro2["name"]+":"+imagemicro2["tag"]
        else:
            fullimagemicro2 = imagemicro2["registry"]+"/"+imagemicro2["project"]+"/"+imagemicro2["name"]+":"+imagemicro2["tag"]
        
        outputdict.update({"bo1": fullimagemicro1, "bo2": fullimagemicro2})

    return outputdict

async def check_resources(resourcesmicro1,resourcesmicro2):
    outputdict = {}
    different = False
    
    #Remove Gi keys
    del resourcesmicro1["cpu"]["request_milicores"]
    del resourcesmicro1["cpu"]["limit_milicores"]
    del resourcesmicro1["memory"]["request_Gi"]
    del resourcesmicro1["memory"]["limit_Gi"]
    
    del resourcesmicro2["cpu"]["request_milicores"]
    del resourcesmicro2["cpu"]["limit_milicores"]
    del resourcesmicro2["memory"]["request_Gi"]
    del resourcesmicro2["memory"]["limit_Gi"]

    for key1,value1 in resourcesmicro1.items():
        try:
            value2 = resourcesmicro2[key1]
            keyok = True
        except KeyError:
            keyok = False
            value2 = "null"

        if keyok:
            if value1 != value2:
                different = True
        else:
            different = True

    if different:
        fullmem1 = f'mem_request: {resourcesmicro1["memory"]["request"]}, mem_limit: {resourcesmicro1["memory"]["limit"]}, cpu_request: {resourcesmicro1["cpu"]["request"]}, cpu_limit: {resourcesmicro1["cpu"]["limit"]}'
        fullmem2 = f'mem_request: {resourcesmicro2["memory"]["request"]}, mem_limit: {resourcesmicro2["memory"]["limit"]}, cpu_request: {resourcesmicro2["cpu"]["request"]}, cpu_limit: {resourcesmicro2["cpu"]["limit"]}'
        outputdict.update({"bo1": fullmem1, "bo2": fullmem2})

    return outputdict

async def get_paused_rollouts(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    
    if entity_id == None:
        entity_id = "spain"

    query = [{}]

    if region != None:
        query.append({"region": region})

    if cluster != None:
        query.append({"cluster": cluster})

    if namespace != None:
        query.append({"namespace": namespace})

    #Check pausedRollouts
    query.append({"pausedrollouts": True})

    fullquery = {"$and": query}

    mongodata = list(mg.find(fullquery))
    
    outputlist = []
    
    for data in mongodata:
        outputdict = await set_output_base_dict(data,destination)

        outputdict.update({
            "microservice": data["microservice"]
        })

        outputlist.append(outputdict)
    
    return outputlist

async def get_mismatched_variables_warning(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    
    ## mismatchedVariables (only for environment variables)
    if entity_id == None:
        entity_id = "spain"

    query = [{}]

    if region != None:
        query.append({"region": region})

    if cluster != None:
        query.append({"cluster": cluster})

    if namespace != None:
        query.append({"namespace": namespace})

    fullquery = {"$and": query}

    mongodata = list(mg.find(fullquery))
    
    outputlist = []
    
    S3_BUCKET_PROJECTS = os.getenv("S3_BUCKET_PROJECTS").split(",")

    for data in mongodata:
        logger.info(f'Checking mismatched variables for microservice: {data["name"]} in namespace: {data["namespace"]}')
        mismatchedvariableslist = []
        try:
            mismatchedvariables = data["mismatchedVariables"]
        except KeyError:
            mismatchedvariables = []

        for elem in mismatchedvariables:
            logger.info(f'Checking mismatched variable: {elem}')
            key = next(iter(elem))
            value = elem[key]
            '''Excepcionado porque el proyecto tiene el sufijo -b ya en el nombre del micro (ajeno al blue-green)
            Excepcionados los S3_BUCKET porque obliga a reiniciar proyectos de seguros cuando hay cambio en estos
            proyectos: bdp, bdples, mcfprc, crtsol'''
            if (data["namespace"] == "sanes-opeadm-pro" and "s-java-50084206-undermodel-opening-b" in data["name"] and key == "spring_application_name") or \
               (data["namespace"] in S3_BUCKET_PROJECTS and "oc-registry-darwin" in data["name"] and key == "S3_BUCKET"):
                continue
            
            mismatchedvariableslist.append(f'{key}: {value}')
            
            
        if mismatchedvariableslist != None and mismatchedvariableslist != []:
            
            microservice = data["kind"]+"-"+data["name"]
                
            mismatchedvariablesstr = ','.join(mismatchedvariableslist)

            outputdict = await set_output_base_dict(data,destination)

            outputdict.update({
                "microservice": microservice,
                "mismatchedVariables": mismatchedvariablesstr
            })
            logger.debug(f'Output dict for mismatched variables: {outputdict}')
            outputlist.append(outputdict)

    return outputlist

async def get_difference_between_regions(entity_id=None,functional_environment="pro",cluster=None,namespace=None,option=None,destination=None):
    if entity_id == None:
        entity_id = "spain"

    query = {}

    if cluster != None:
        query.update({"cluster": cluster})

    no_high_availability_micros = os.getenv("MICROS_NO_HIGH_AVAILABILITY").split(",")
    no_high_availability_namespaces = os.getenv("NAMESPACES_NO_HIGH_AVAILABILITY").split(",")

    if namespace != None:
        query.update({"namespace": namespace})
    else:
        query.update({"namespace": {"$not": {"$in": no_high_availability_namespaces}}})


    query.update({"name": {"$not": {"$in": no_high_availability_micros}}})

    query.update({"region": {"$regex": "1"}})
    mongodataregion1 = list(mg.find({"$and": [query]}))
    del query["region"]
    query.update({"region": {"$regex": "2"}})
    mongodataregion2 = list(mg.find({"$and": [query]}))
    
    outputlist = []

    for data1 in mongodataregion1:
        logger.info('Checking microservice')
        positionmicro = None
        microservice1 = data1["kind"]+ "-" +data1["id"]
        if any(micro in microservice1 for micro in no_high_availability_micros):
            continue

        logger.info(f'Microservice: {microservice1}')
        microservice2 = microservice1.replace("bo1-san","bo2-san")
        microservice2 = microservice2.replace("weu1-san","weu2-san")
        microservice2 = microservice2.replace("bo1-sfc","bo2-sfc")
        microservice2 = microservice2.replace("weu1-sfc","weu2-sfc")
        for index,data2 in enumerate(mongodataregion2):
            logger.debug('Checking microservice in region 2')
            if microservice2 == data2["kind"]+"-"+ data2["id"]:
                positionmicro = index
                break
        
        if positionmicro != None:
            match option:
                case "image":
                    datadict = await check_image(data1["image"],mongodataregion2[positionmicro]["image"])    
                case "envVar":
                    datadict = await check_env_var(data1["envVar"],mongodataregion2[positionmicro]["envVar"])
                case "resources":
                    datadict = await check_resources(data1["resources"],mongodataregion2[positionmicro]["resources"])

        else:
            datadict = {"bo1": "Micro exists", "bo2": "Micro doesn't exist"}
                    
        if datadict != {}:
            outputdict = await set_output_base_dict(data=data1,destination=destination)

            outputdict.update({"microservice": data1["kind"] + "-" + data1["name"]})
            outputdict.update(datadict)
            
            outputlist.append(outputdict)

    return outputlist

async def get_replicas_warning(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Get the microservices with different desired and actual replicas.'''
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
    
    outputlist = []

    for data in mongodata:
        logger.info(f'Checking microservice: {data["kind"]}-{data["name"]} for desired and actual replicas.')
        desiredreplicas = data['replicas']["desiredreplicas"]
        actualreplicas = data['replicas']["actualreplicas"]
        if desiredreplicas != actualreplicas:
            logger.info(f'Microservice {data["kind"]}-{data["name"]} has different desired and actual replicas: {desiredreplicas} vs {actualreplicas}')
            outputdict = await set_output_base_dict(data, destination)

            outputdict.update({"microservice": data["kind"] + "-" + data["name"]})
            replicas = f'Desired Replicas: {desiredreplicas}, Actual Replicas: {actualreplicas}'

            outputdict.update({"replicas": replicas})
                
            outputlist.append(outputdict)

    return outputlist