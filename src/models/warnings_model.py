from pydantic import BaseModel, Field
from typing import Optional

class WarningModel(BaseModel):
    entity_id: Optional[str] = Field(default="spain",json_schema_extra={"description":"Entity"})
    functional_environment: Optional[str] = None
    cluster: Optional[str] = None
    region: Optional[str] = None
    namespace: Optional[str] = None