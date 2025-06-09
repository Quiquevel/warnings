'''This module defines the WarningModel class used for handling warning data in the application.'''
from os import getenv
from shuttlelib.openshift.client import OpenshiftClient
from shuttlelib.utils.logger import logger

entity_id = getenv("ENTITY_ID", "spain")
if entity_id is None:
    logger.error("ENTITY_ID environment variable is not set")
    raise ValueError("ENTITY_ID environment variable is not set")

logger.info(f"Initializing OpenshiftClient with entity_id: {entity_id}")
client = OpenshiftClient(entity_id=entity_id)

def getenvironmentsclusterslist():
    """Get the list of environments, clusters, and regions from OpenshiftClient."""

    logger.info("Starting getenvironmentsclusterslist function")
    environment_list = []
    cluster_dict = {}
    region_dict = {}

    try:
        for environment in client.clusters.keys():
            logger.info(f"Processing environment: {environment}")
            environment_list.append(environment.lower())

            clusters = list(client.clusters[environment])
            cluster_dict[environment.lower()] = sorted(set(x.lower() for x in clusters))
            logger.info(f"Clusters found for {environment}: {clusters}")

            for cluster in clusters:
                clusterdata = client.clusters[environment][cluster]
                regions = list(clusterdata)

                if environment.lower() not in region_dict:
                    region_dict[environment.lower()] = {}

                region_dict[environment.lower()][cluster.lower()] = sorted(set(region.lower() for region in regions))
                logger.info(f"Regions found for cluster {cluster} in environment {environment}: {regions}")

        environment_list = sorted(environment_list)
        logger.info(f"Final environment list: {environment_list}")

        return environment_list, cluster_dict, region_dict

    except Exception as e:
        logger.error(f"Error in getenvironmentsclusterslist: {str(e)}", exc_info=True)
        return [], {}, {}
    
def getenvironmentsclustersregionslist():
    '''Get the list of environments, clusters, and regions from OpenshiftClient, including upper case and special values.'''
    environmentlist = []
    clusterlist = []
    regionlist = []
    clusterlistaux = []
    regionlistaux = []

    environmentlist = list(client.clusters.keys())

    for environment in environmentlist:
        clusterlistaux = list(client.clusters[environment].keys())
        for cluster in clusterlistaux:
            regionlistaux = list(client.clusters[environment][cluster].keys())
            regionlist.extend(regionlistaux)
        clusterlist.extend(clusterlistaux)

    environmentlist.extend([x.upper() for x in environmentlist])
    environmentlist.extend(["all", "ALL"])

    clusterlist.extend([x.upper() for x in clusterlist])
    clusterlist.extend(["all", "ALL"])
    clusterlist = list(set(clusterlist))
    clusterlist.sort()

    regionlist.extend([x.upper() for x in regionlist])
    regionlist.extend(["both", "BOTH"])
    regionlist = list(set(regionlist))
    regionlist.sort()

    return environmentlist, clusterlist, regionlist
