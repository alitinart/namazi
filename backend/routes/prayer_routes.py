from fastapi import APIRouter
from pydantic import BaseModel
from ..models.prayer_model import Prayer

from ..services.prayer_service import *

router = APIRouter()

@router.get("/prayers")
def prayers(lat: float, lng: float, method: str = "ISNA", date: str = date.today()):
    times = get_prayers(lat, lng, method=method, prayer_date=date)
    return times