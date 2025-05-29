"""
This module contains the main FastAPI application for the microservice.
"""
from src.app.config.composer_config import config
from fastapi import FastAPI
from darwin_composer.DarwinComposer import DarwinComposer
from src.resources.routers import routers


app = FastAPI()

DarwinComposer(app, config=config, routers=routers)

