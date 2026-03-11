from typing import Optional

from fastapi import APIRouter, Depends

from app.api.dependencies import get_chat
from app.api.schemas.requests import ChatRequest
from app.api.schemas.responses import ChatResponse, OutfitCardResponse, PlaceCardResponse
from app.application.use_cases.chat import Chat

router = APIRouter(prefix="/chat", tags=["chat"])


@router.post("", response_model=ChatResponse)
async def chat(
    body: ChatRequest,
    use_case: Chat = Depends(get_chat),
) -> ChatResponse:
    reply, conversation_id, structured_data = await use_case.execute(
        user_id=body.user_id,
        message=body.message,
        conversation_id=body.conversation_id,
    )

    places: Optional[list[PlaceCardResponse]] = None
    outfit: Optional[OutfitCardResponse] = None

    if structured_data:
        raw_places = structured_data.get("places")
        if raw_places:
            places = [PlaceCardResponse(**p) for p in raw_places]

        raw_outfit = structured_data.get("outfit")
        if raw_outfit:
            outfit = OutfitCardResponse(**raw_outfit)

    return ChatResponse(
        conversation_id=conversation_id,
        reply=reply,
        places=places,
        outfit=outfit,
    )
