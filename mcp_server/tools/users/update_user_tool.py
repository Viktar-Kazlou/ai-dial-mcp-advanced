from typing import Any

from models.user_info import UserUpdate
from tools.users.base import BaseUserServiceTool


class UpdateUserTool(BaseUserServiceTool):

    @property
    def name(self) -> str:
        return "update_user"

    @property
    def description(self) -> str:
        return "Updates an existing user by ID with provided fields"

    @property
    def input_schema(self) -> dict[str, Any]:
        return {
            "type": "object",
            "properties": {
                "id": {
                    "type": "number",
                    "description": "User ID that should be updated"
                },
                "new_info": UserUpdate.model_json_schema()
            },
            "required": ["id", "new_info"]
        }

    async def execute(self, arguments: dict[str, Any]) -> str:
        user_id = int(arguments["id"])
        user_update_model = UserUpdate.model_validate(arguments["new_info"])
        return await self._user_client.update_user(user_id, user_update_model)

