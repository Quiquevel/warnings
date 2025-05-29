""" Get warnings of hpas. """

from pydantic import BaseModel, Field
from typing import Optional
from src.models.warnings_model import WarningModel

class HpasRequest(WarningModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity",'examples': ['spain','sgt','gsc']})
    functional_environment: Optional[str] = Field(default="pro",json_schema_extra={"description":"Environment",'examples': ['pro','pre','dev']})
    destination: Optional[str] = Field(default="swagger",json_schema_extra={"description":"what is the report for? itsm, swagger...",'examples': ['itsm','swagger']})

class HpasResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":"Devops owner of the detected project",'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    namespace: str = Field(json_schema_extra={"description":"namespace",'examples': ["sanes-shuttle-pro"]})
    hpaname: str = Field(json_schema_extra={"description":"hpaname",'examples': ["darwin-gatewayweb-g"]})
    scaleTargetKind: str = Field(json_schema_extra={"description":"scale target kind",'examples': ["deployment"]})
    scaleTargetName: str = Field(json_schema_extra={"description":"scale target name",'examples': ["darwin-gatewayweb-g"]})
    scaleTargetApiVersion: str = Field(json_schema_extra={"description":"scale target apiVersion",'examples': ["apps/v1"]})
    min_replicas: int = Field(json_schema_extra={"description":"min replicas configured",'examples': ["5"]})
    max_replicas: int = Field(json_schema_extra={"description":"max replicas configured",'examples': ["5"]})

class HpasUnableResponse(BaseModel):
    devops: str = Field(json_schema_extra={"description":"Devops owner of the detected project",'examples': ['Peter Parker']})  
    cluster: str = Field(json_schema_extra={"description":"cluster",'examples': ["ocp5azure"]})
    region: str = Field(json_schema_extra={"description":"region",'examples': ["weu1"]})
    namespace: str = Field(json_schema_extra={"description":"namespace",'examples': ["sanes-shuttle-pro"]})
    hpaname: str = Field(json_schema_extra={"description":"hpaname",'examples': ["darwin-gatewayweb-g"]})
    scaleTargetKind: str = Field(json_schema_extra={"description":"scale target kind",'examples': ["deployment"]})
    scaleTargetName: str = Field(json_schema_extra={"description":"scale target name",'examples': ["darwin-gatewayweb-g"]})
    scaleTargetApiVersion: str = Field(json_schema_extra={"description":"scale target apiVersion",'examples': ["apps/v1"]})
    ableToScale: str = Field(json_schema_extra={"description":"reason why hpa is unable to scale",'examples': ["Unable to scale. Reason: the HPA controller was unable to get the target's current scale: deployments/scale.apps 'darwin-gatewayweb-g' not found"]})

