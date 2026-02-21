from typing import Any

from models.user_info import UserCreate
from tools.users.base import BaseUserServiceTool


class CreateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "add_user"

    @property
    def description(self) -> str:
        return "Creates a new user in the users management service"

    @property
    def input_schema(self) -> dict[str, Any]:
        return UserCreate.model_json_schema()

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_create_model = UserCreate.model_validate(arguments)
        return await self._user_client.add_user(user_create_model)