""" Get warnings of microservices. """

from pydantic import BaseModel, Field
from typing import Optional
from src.models.warnings_model import WarningModel

class QuotasRequest(WarningModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity",'examples': ['spain','sgt','gsc']})
    functional_environment: Optional[str] = Field(default="pro",json_schema_extra={"description":"Environment",'examples': ['pro','pre','dev']})
    # cluster: Optional[str] = Field(default=None,json_schema_extra={"description":"Cluster",'examples': ['dmzbdarwin','opc05azure','prodarwin']})
    # region: Optional[str] = Field(default=None,json_schema_extra={"description":"Region",'examples': ['bo1','bo2']})
    #namespace: Optional[str] = Field(default=None,json_schema_extra={"description":"Namespace for getting the warning",'examples': ['sanes-shuttle-pro']})
    destination: Optional[str] = Field(default="swagger",json_schema_extra={"description":"what is the report for? itsm, swagger...",'examples': ['itsm','swagger']})

class QuotasResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":"Devops owner of the detected project",'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    namespace: str = Field(json_schema_extra={"description":"namespace",'examples': ["sanes-shuttle-pro"]})
    quotaswarning: str = Field(json_schema_extra={"description":"quotas warning",'examples': ["replicaSets"]})
    quotasexceeded: str = Field(json_schema_extra={"description":"quotas exceeded",'examples': ["replicaSets"]})
