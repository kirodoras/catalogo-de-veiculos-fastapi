from fastapi import APIRouter

from api.v1.endpoints import veiculo
from api.v1.endpoints import admin

api_router = APIRouter()
api_router.include_router(veiculo.router, prefix='/veiculos', tags=['veiculos'])
api_router.include_router(admin.router, prefix='/admin', tags=['admin'])