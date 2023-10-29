import aiohttp
from aiohttp.client import ContentTypeError

from src.users.models import User
from src.vr_api.urls import SIGNUP, SINGIN, PROFILE, REFRESH


class VRAuthService:
    header: str = {"ngrok-skip-browser-warning": "69420"}

    def __init__(self, user: User) -> None:
        self.user = user

    async def auth(self):
        credentials = {"email": self.user.email, "password": self.user.password}
        try:
            token_pairs = await self.signup(credentials)
        except ContentTypeError:
            token_pairs = await self.signin(credentials)
        return token_pairs

    async def signup(self, data: dict[str, str]):
        async with aiohttp.ClientSession() as session:
            async with session.post(SIGNUP, json=data) as response:
                return await response.json()

    async def signin(self, data: dict[str, str]):
        async with aiohttp.ClientSession(headers=self.header) as session:
            async with session.post(SINGIN, json=data) as response:
                return await response.json()

    async def profile(self, token):
        pass