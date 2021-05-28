#!/usr/bin/env python3
from fastapi import APIRouter

from api.v1.routers import users


router = APIRouter(prefix='/api/v1')  # prefix='/api/v1'

router.include_router(users.router)
