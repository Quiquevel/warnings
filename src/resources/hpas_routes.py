"""
This module contains the implementation of the FastAPI resources for the xxxxxxxxx and xxxxxxxxx endpoints.
"""
import logging
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from src.services.hpas import check_min_man, check_unable_condition 
from docs.openapi.hpas_doc import HpasRequest, HpasResponse

hpaswarnings = APIRouter(tags=["hpas"],prefix="/api/v1/warnings")

@hpaswarnings.post("/hpa_minmax_equal",response_model=HpasResponse)
async def hpas_min_max (hpas:HpasRequest, request:Request):
    """
    Endpoint for getting hpas min=max warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the check_Min_Man function.
    
    """
    
    result = await check_min_man(hpas.entity_id, hpas.functional_environment, hpas.cluster, hpas.region, hpas.namespace, hpas.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)

@hpaswarnings.post("/get_hpa_unabletoscale",response_model=HpasResponse)
async def hpa_unabletoscale (hpas:HpasRequest, request:Request):
    """
    Endpoint for getting hpas unabletoscale warning.
    
    This endpoint receives a request with the following parameters:
    - entity_id: str
    - functional_environment: str
    - cluster: str
    - region: str
    - namespace: str
    
    It returns a JSON response with the result of the check_unable_condition function.
    
    """
    
    result = await check_unable_condition(hpas.entity_id, hpas.functional_environment, hpas.cluster, hpas.region, hpas.namespace,hpas.destination)

    return JSONResponse(content={
                                    "result": result
                                }, status_code=200)