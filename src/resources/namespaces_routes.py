"""
This module contains the implementation of the FastAPI resources for the xxxxxxxxx and xxxxxxxxx endpoints.
"""
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.commonfunctions import get_wrong_routing_dns
from docs.openapi.namespaces_doc import NamespacesRequest, NamespacesResponse

namespaceswarnings = APIRouter(tags=["namespaces"],prefix="/api/v1/warnings")

@namespaceswarnings.post("/get_wrong_routing_dns",response_model=NamespacesResponse)
async def wrong_routing_dns(namespaces:NamespacesRequest, request:Request):
    """
    Endpoint for getting services warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the get_wrong_routing_dns function.
    
    """
    
    result = await get_wrong_routing_dns(namespaces.entity_id, namespaces.functional_environment, namespaces.cluster, namespaces.region, namespaces.namespace,namespaces.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)