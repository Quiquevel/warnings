import requests
import json
from shuttlelib.utils.logger import logger

async def get_data_from_knowledge(namespace):
    urlapi = 'https://sgt-apm2123-knowledge-sanes-shuttle-pro.apps.san01darwin.san.pro.bo1.paas.cloudcenter.corp'
    endpoint = '/api/v1/knowledge'
    option = '/detailnamespace'


    body = {
        'namespace': namespace
    }

    answer = requests.post(urlapi+endpoint+option, json=body, verify=False)
    logger.info(f'Knowledge API response for namespace {namespace}: {answer.status_code} - {answer.text}')
    # Check if the response is successful
    # If the response is successful, parse the JSON data
    
    if answer.status_code == 200:
        data = json.loads(answer.text)
    else:
        data = []

    return data

async def get_devops_list(namespaceinfo,namespace,destination="swagger"):
    devopslist = []
    try:
        for devops in namespaceinfo[0]["devops"]:
            if destination == "itsm":
                devopslist.append(devops["uid"])
            else:
                devopslist.append(devops["name"])
    except Exception as e:
        logger.info(f'No Devops was gotten from knowledge for {namespace}: {e} ')

    return devopslist