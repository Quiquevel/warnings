from .microservices_routes import microswarnings
from .services_routes import serviceswarnings
from .namespaces_routes import namespaceswarnings
from .hpas_routes import hpaswarnings
from .quotas_routes import quotaswarnings
from darwin_composer.DarwinComposer import RouteClass

routers = [
    RouteClass(microswarnings,["microservices"]),
    RouteClass(serviceswarnings,["services"]),
    RouteClass(namespaceswarnings,["namespaces"]),
    RouteClass(hpaswarnings,["hpas"]),
    RouteClass(quotaswarnings,["quotas"])
]
