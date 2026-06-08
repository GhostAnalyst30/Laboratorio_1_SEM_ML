from fastapi import APIRouter

from .apartments import router as apartments_router
from .towers import router as towers_router
from .simulation import router as simulation_router
from .analytics import router as analytics_router
from .community import router as community_router
from .export import router as export_router

router = APIRouter(prefix="/api")

router.include_router(apartments_router)
router.include_router(towers_router)
router.include_router(simulation_router)
router.include_router(analytics_router)
router.include_router(community_router)
router.include_router(export_router)
