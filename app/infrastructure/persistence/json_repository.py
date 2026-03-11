import json
from pathlib import Path

from app.domain.entities.user_profile import UserProfile
from app.domain.exceptions import ProfileNotFound
from app.domain.services.user_repository import UserRepository


class JsonUserRepository(UserRepository):
    def __init__(self, data_dir: str):
        self._file_path = Path(data_dir) / "users.json"
        self._ensure_file()

    def _ensure_file(self) -> None:
        self._file_path.parent.mkdir(parents=True, exist_ok=True)
        if not self._file_path.exists():
            self._file_path.write_text("{}")

    def _read(self) -> dict:
        return json.loads(self._file_path.read_text())

    def _write(self, data: dict) -> None:
        self._file_path.write_text(json.dumps(data, indent=2))

    async def get_profile(self, user_id: str) -> UserProfile:
        data = self._read()
        if user_id not in data:
            raise ProfileNotFound(user_id)
        return UserProfile(**data[user_id])

    async def save_profile(self, profile: UserProfile) -> UserProfile:
        data = self._read()
        data[profile.user_id] = profile.model_dump()
        self._write(data)
        return profile

    async def update_profile(self, user_id: str, updates: dict) -> UserProfile:
        data = self._read()
        if user_id not in data:
            raise ProfileNotFound(user_id)
        data[user_id].update(updates)
        self._write(data)
        return UserProfile(**data[user_id])
