""" Get warnings of microservices. """

from pydantic import BaseModel, Field
from typing import Optional
from src.models.warnings_model import WarningModel

DEVOPS_OWNER = "Devops owner of the detected project"

class NamespacesRequest(WarningModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity",'examples': ['spain','sgt','gsc']})
    functional_environment: Optional[str] = Field(default="pro",json_schema_extra={"description":"Environment",'examples': ['pro','pre','dev']})
    namespace: Optional[str] = Field(default=None,json_schema_extra={"description":"Namespace for getting the warning",'examples': ['sanes-shuttle-pro']})
    destination: Optional[str] = Field(default="swagger",json_schema_extra={"description":"what is the report for? itsm, swagger...",'examples': ['itsm','swagger']})

class NamespacesResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":DEVOPS_OWNER,'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    configuration_object: str = Field(json_schema_extra={"description":"object where wrong routing is",'examples': ["configuration-service-g"]})
    file: str = Field(json_schema_extra={"description":"file where the wrong routing is",'examples': ["application.yaml"]})
    wrong_routing: str = Field(json_schema_extra={"description":"wrong routing",'examples': ["isban.dev.corp"]})
