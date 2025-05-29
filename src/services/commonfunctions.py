from src.services.namespaces import get_wrong_routing_dnss_configurationservice
from src.services.configmaps import get_wrong_routing_dns_configmaps
from shuttlelib.utils.logger import logger

async def get_wrong_routing_dns(entity_id=None,functional_environment="pro",cluster=None,region=None,namespace=None,destination=None):
    '''Get the wrong routing DNS for a given entity_id, functional_environment, cluster, region, namespace, and destination.'''
    logger.info(
        f"Getting wrong routing DNS for entity_id: {entity_id}, "
        f"functional_environment: {functional_environment}, "
        f"cluster: {cluster}, region: {region}, "
        f"namespace: {namespace}, destination: {destination}"
    )
    configuration_service_list =  await get_wrong_routing_dnss_configurationservice(entity_id,functional_environment,cluster,region,namespace)
    configmaps_list = await get_wrong_routing_dns_configmaps(entity_id,functional_environment,cluster,region,namespace)
    outputlist = configuration_service_list + configmaps_list

    return outputlist