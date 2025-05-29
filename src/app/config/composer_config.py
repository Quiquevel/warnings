from version import __version__
from ..config import global_config

description = '''Proactively identify and warn about potential issues in OpenShift projects to prevent critical production incidents.'''

config = {
     "version": __version__,
     "cors": {
          "enable": False
     },
     "openapi": {
          "enable": True,
          "title": "SRE Warnings",
          "description": description,
          "contact": {
               "name": "Carlos Murcia Ruiz",
               "url": "carlosfernando.murcia@gruposantander.com"
          }
     },
     "i18n": {
          "enable": False,
          "fallback": "en",
     }
}
