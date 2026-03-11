from fastapi import APIRouter, Depends

from app.api.dependencies import get_onboard_user, get_get_user_profile, get_update_user_profile
from app.api.schemas.requests import ProfileCreate, ProfileUpdate
from app.api.schemas.responses import ProfileResponse
from app.application.use_cases.get_user_profile import GetUserProfile
from app.application.use_cases.onboard_user import OnboardUser
from app.application.use_cases.update_user_profile import UpdateUserProfile

router = APIRouter(prefix="/profile", tags=["profile"])


@router.post("", response_model=ProfileResponse, status_code=201)
async def create_profile(
    body: ProfileCreate,
    use_case: OnboardUser = Depends(get_onboard_user),
) -> ProfileResponse:
    from app.domain.entities.user_profile import UserProfile
    profile = await use_case.execute(UserProfile(**body.model_dump()))
    return ProfileResponse(**profile.model_dump())


@router.get("/{user_id}", response_model=ProfileResponse)
async def get_profile(
    user_id: str,
    use_case: GetUserProfile = Depends(get_get_user_profile),
) -> ProfileResponse:
    profile = await use_case.execute(user_id)
    return ProfileResponse(**profile.model_dump())


@router.patch("/{user_id}", response_model=ProfileResponse)
async def update_profile(
    user_id: str,
    body: ProfileUpdate,
    use_case: UpdateUserProfile = Depends(get_update_user_profile),
) -> ProfileResponse:
    updates = {k: v for k, v in body.model_dump().items() if v is not None}
    profile = await use_case.execute(user_id, updates)
    return ProfileResponse(**profile.model_dump())
