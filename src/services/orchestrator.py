from services.microservices import get_mismatched_variables_warning
from services.itsm import create_itsm
from shuttlelib.utils.logger import logger

async def get_warnings_for_itsm(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None):
    warning_list = await get_mismatched_variables_warning(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None)
    for warning in warning_list[0:1]:
        logger.info(f'Processing warning: {warning}')
        event_id = f'{warning["cluster"]}-{warning["region"]}-{warning["namespace"]}-{warning["microservice"]}'
        event_description = f'''The microservice {event_id} has mismatched variables (there is no blue/green good match). 
                                {warning["microservice"]} --> {warning["mismatchedVariables"]}
                            '''
        
        micro = warning["microservice"]
        microservice = micro[micro.find("-")+1:]
        element = f'{warning["namespace"]}/{microservice}'
        dict_for_istm = {   
                            "namespace": warning["namespace"],
                            "microservice": microservice,
                            "cluster": warning["cluster"],
                            "region": warning["region"],
                            "event_id": event_id,
                            "event_description": event_description,
                            "GrupoResponsable": "SGT_OPS Team Santander",
                            "element": element,
                        }
        logger.info(f'Creating ITSM for {dict_for_istm}')
        await create_itsm(dict_for_istm,warning_type = "MismatchedVariables")