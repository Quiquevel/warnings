import aiohttp
from src.services.clientunique import client
from shuttlelib.utils.logger import logger

async def create_itsm(dict_for_istm,warning_type):
    '''Create an ITSM problem based on the provided dictionary and warning type.'''
    token =  client.clusters["token"]
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {token}'
    }    
    pid = f'{warning_type}-{dict_for_istm["cluster"]}-{dict_for_istm["region"]}-{dict_for_istm["namespace"]}-{dict_for_istm["microservice"]}'
    data = {
        "origin": "SHUTTLE_INTEGRATION",
        "state": "OPEN",
        "pid": pid,
        "problemtitle": f'Shuttle warning: {dict_for_istm["event_id"]}',
        "problemdetailstext": dict_for_istm["event_description"],
        "problemdetailsjson": {
            "Namespace": dict_for_istm["namespace"],
            "GrupoResponsable": dict_for_istm["GrupoResponsable"],
            "assigned_to": "n750634@santanderglobaltech.com",
            "Empresa": "Santander Digital Services",
            "Entorno": "Production",
            "Element": dict_for_istm["element"]
        }
    }
    logger.info(f"Creating ITSM problem with data: {data}")
    async with aiohttp.ClientSession() as session:
        async with session.post("https://alma-le.sgtech.corp/v2/problems?return_uuid=true",headers=headers,ssl=False,json=data) as response:
            print(response.status)