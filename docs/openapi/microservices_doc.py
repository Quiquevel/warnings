""" Get warnings of microservices. """

from pydantic import BaseModel, Field
from typing import Optional
from src.models.warnings_model import WarningModel

DEVOPS_OWNER = "Devops owner of the detected project"

class MicroservicesRequest(WarningModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity",'examples': ['spain','sgt','gsc']})
    functional_environment: Optional[str] = Field(default="pro",json_schema_extra={"description":"Environment",'examples': ['pro','pre','dev']})
    namespace: Optional[str] = Field(default=None,json_schema_extra={"description":"Namespace for getting the warning",'examples': ['sanes-shuttle-pro']})
    destination: Optional[str] = Field(default="swagger",json_schema_extra={"description":"what is the report for? itsm, swagger...",'examples': ['itsm','swagger']})

class MismatchedVariablesResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":DEVOPS_OWNER,'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    microservice: str = Field(json_schema_extra={"description":"microservice",'examples': ["configuration-service-g"]})
    mismatchedVariables: str = Field(json_schema_extra={"description":"mismatched variable found",'examples': ["darwin-suffix: -b"]})

class PausedRolloutsResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":DEVOPS_OWNER,'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    microservice: str = Field(json_schema_extra={"description":"microservice",'examples': ["configuration-service-g"]})

class MicroservicesPausedResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":DEVOPS_OWNER,'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    microservice: str = Field(json_schema_extra={"description":"microservice",'examples': ["configuration-service-g"]})


class MicroservicesDiffRequest(BaseModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity",'examples': ['spain','sgt','gsc']})
    functional_environment: Optional[str] = Field(default="pro",json_schema_extra={"description":"Environment",'examples': ['pro','pre','dev']})
    cluster: Optional[str] = Field(default=None,json_schema_extra={"description":"Cluster",'examples': ['dmzbdarwin','opc05azure','prodarwin']})
    region: Optional[str] = Field(default=None,json_schema_extra={"description":"Region",'examples': ['bo1','bo2']})
    namespace: Optional[str] = Field(default=None,json_schema_extra={"description":"Namespace for getting the warning",'examples': ['sanes-shuttle-pro']})
    option: str = Field(json_schema_extra={"description":"Option to get the difference between regions",'examples': ['image', 'envVar','resources']})
    destination: Optional[str] = Field(default="swagger",json_schema_extra={"description":"what is the report for? itsm, swagger...",'examples': ['itsm','swagger']})

class MicroservicesDiffResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":DEVOPS_OWNER,'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    microservice: str = Field(json_schema_extra={"description":"microservice",'examples': ["configuration-service-g"]})
    bo1: str = Field(json_schema_extra={"description":"values for bo1 region",'examples': ["values of bo1"]})
    bo2: str = Field(json_schema_extra={"description":"values for bo2 region",'examples': ["values of bo2"]})