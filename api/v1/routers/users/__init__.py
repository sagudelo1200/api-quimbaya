#!/usr/bin/env python3
from fastapi import APIRouter

from . import (
    user, familia, manada, tropa, sociedad, clan, jefatura, concejo
)

router = APIRouter()

router.include_router(user.router)
router.include_router(familia.router)
router.include_router(manada.router)
router.include_router(tropa.router)
router.include_router(sociedad.router)
router.include_router(clan.router)
router.include_router(jefatura.router)
router.include_router(concejo.router)
