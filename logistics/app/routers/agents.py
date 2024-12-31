# app/routers/agents.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def get_agents():
    return {"message": "List of agents"}
