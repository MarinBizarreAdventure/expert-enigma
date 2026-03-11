from fastapi import APIRouter, Depends

from app.api.schemas.requests import RecommendationRequest
from app.api.schemas.responses import RecommendationResponse

router = APIRouter(prefix="/recommend", tags=["recommend"])


@router.post("", response_model=RecommendationResponse)
async def recommend(body: RecommendationRequest) -> RecommendationResponse:
    raise NotImplementedError
