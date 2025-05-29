from src.services.devops import get_data_from_knowledge,get_devops_list
from shuttlelib.utils.logger import logger

async def set_output_base_dict(data,destination):
    namespace = data["namespace"]
    cluster = data["cluster"]
    region = data["region"]
    namespaceinfo = await get_data_from_knowledge(namespace[:-4])
    devopslist = await get_devops_list(namespaceinfo,namespace,destination)

    logger.debug(f"DevOps list for namespace {namespace}: {devopslist}")

    outputdict = {
        "devops": ",".join(devopslist),
        "cluster": cluster,
        "region": region,
        "namespace": namespace,
    }
    logger.debug(f"Output dict for namespace {namespace}: {outputdict}")
    return outputdict