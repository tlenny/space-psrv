from fastapi import APIRouter
from src.q7 import DataQuery


router = APIRouter(
    prefix="/q7",
    tags=["q7"],
    dependencies=[],
    responses={404: {"description": "Not found"}},
)


@router.get("/env")
async def get_env_list():
    return DataQuery.get_env_list()


@router.get("/tenant")
async def get_tenant_list(key, global_env, env_type):
    return DataQuery.get_tenant_list(key, global_env, env_type)


@router.get("/env/{env_id}")
async def get_env_list(env_id):
    return DataQuery.get_env_config(env_id)



