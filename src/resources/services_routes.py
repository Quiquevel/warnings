"""
This module contains the implementation of the FastAPI resources for the xxxxxxxxx and xxxxxxxxx endpoints.
"""
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.services import get_routing_services, get_services_routing_nowhere
from docs.openapi.services_doc import ServicesRequest, ServicesResponse

serviceswarnings = APIRouter(tags=["services"],prefix="/api/v1/warnings")

@serviceswarnings.post("/get_services",response_model=ServicesResponse)
async def routing_services(services:ServicesRequest, request:Request):
    """
    Endpoint for getting services warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the get_routing_services function.
    
    """
    
    result = await get_routing_services(services.entity_id, services.functional_environment, services.cluster, services.region, services.namespace,services.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)

@serviceswarnings.post("/get_services_routing_nowhere",response_model=ServicesResponse)
async def routing_nowhere_services(services:ServicesRequest, request:Request):
    """
    Endpoint for getting services warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the get_services_routing_nowhere function.
    
    """
    
    result = await get_services_routing_nowhere(services.entity_id, services.functional_environment, services.cluster, services.region, services.namespace, services.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)