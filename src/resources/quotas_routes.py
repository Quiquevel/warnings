"""
This module contains the implementation of the FastAPI resources for the xxxxxxxxx and xxxxxxxxx endpoints.
"""
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.quotas import get_quotas
from docs.openapi.quotas_doc import QuotasRequest, QuotasResponse

quotaswarnings = APIRouter(tags=["quotas"],prefix="/api/v1/warnings")

@quotaswarnings.post("/get_quotas",response_model=QuotasResponse)
async def quotas(quotas:QuotasRequest, request:Request):
    """
    Endpoint for getting quotas warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the get_quotas function.
    
    """
    
    result = await get_quotas(quotas.entity_id, quotas.functional_environment, quotas.cluster, quotas.region, quotas.namespace,quotas.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)
