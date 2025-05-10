from handlers.start import router as start_router
from handlers.conference import router as conference_router
from handlers.registration import router as registration_router
from handlers.services import router as services_router
from handlers.materials import router as materials_router
from handlers.casinos import router as casinos_router
from handlers.responsible import router as responsible_router

__all__ = [
    'start_router',
    'conference_router',
    'registration_router',
    'services_router',
    'materials_router',
    'casinos_router',
    'responsible_router'
]