"""
This module contains the implementation of the FastAPI resources for the xxxxxxxxx and xxxxxxxxx endpoints.
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.microservices import get_mismatched_variables_warning, get_difference_between_regions,get_paused_rollouts
from docs.openapi.microservices_doc import MicroservicesRequest, MismatchedVariablesResponse, PausedRolloutsResponse, MicroservicesDiffResponse, MicroservicesDiffRequest

microswarnings = APIRouter(tags=["microservices"],prefix="/api/v1/warnings")

@microswarnings.post("/get_mismatched_variables",response_model=MismatchedVariablesResponse)
async def mismatched_variables(mismatchedvariables:MicroservicesRequest, request:Request):
    """
    Endpoint for getting mismatched variables warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the get_mismatched_variables_warning function.
    
    """
    result = await get_mismatched_variables_warning(mismatchedvariables.entity_id, mismatchedvariables.functional_environment, mismatchedvariables.cluster, mismatchedvariables.region, mismatchedvariables.namespace,mismatchedvariables.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)

@microswarnings.post("/get_difference_btw_regions",response_model=MicroservicesDiffResponse)
async def micros_r1r2_diff(difference:MicroservicesDiffRequest, request:Request):
    """
    Endpoint for getting regions differences warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    - option: str 
        - image
        - envVar
        - resources
    
    It returns a JSON response with the result of the get_difference_between_regions function.
    
    """
    
    result = await get_difference_between_regions(difference.entity_id, difference.functional_environment, difference.cluster, difference.namespace,difference.option,difference.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)

@microswarnings.post("/get_paused_rollouts",response_model=PausedRolloutsResponse)
async def micros_paused(micro_paused:MicroservicesRequest, request:Request):
    """
    Endpoint for getting paused rollouts warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the get_paused_rollouts function.
    
    """
    
    result = await get_paused_rollouts(micro_paused.entity_id, micro_paused.functional_environment, micro_paused.cluster, micro_paused.namespace,micro_paused.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)
