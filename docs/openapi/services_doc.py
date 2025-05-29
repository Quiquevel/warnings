""" Get warnings of services. """

from pydantic import BaseModel, Field
from typing import Optional
from src.models.warnings_model import WarningModel

class ServicesRequest(WarningModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity",'examples': ['spain','sgt','gsc']})
    functional_environment: Optional[str] = Field(default="pro",json_schema_extra={"description":"Environment",'examples': ['pro','pre','dev']})
    destination: Optional[str] = Field(default="swagger",json_schema_extra={"description":"what is the report for? itsm, swagger...",'examples': ['itsm','swagger']})

class ServicesResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":"Devops owner of the detected project",'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    namespace: str = Field(json_schema_extra={"description":"namespace",'examples': ["sanes-shuttle-pro"]})
    microservice: str = Field(json_schema_extra={"description":"microservice",'examples': ["configuration-service-g"]})

class ServicesNowhereResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":"Devops owner of the detected project",'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    namespace: str = Field(json_schema_extra={"description":"namespace",'examples': ["sanes-shuttle-pro"]})
    service: str = Field(json_schema_extra={"description":"service",'examples': ["b-g-configuration-service"]})
    selectors: str = Field(json_schema_extra={"description":"selectors",'examples': ["configuration-service-g"]})
