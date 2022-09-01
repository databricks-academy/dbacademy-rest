from typing import Any, Dict, List, Literal
from dbacademy.rest.common import ApiClient
from dbacademy.rest.permissions.crud import PermissionsCrud

__all__ = ["Tokens"]

# noinspection PyProtectedMember
from dbacademy.rest.permissions.crud import What, PermissionLevel

class Tokens(PermissionsCrud):
    valid_permissions = ["CAN_USE", "CAN_MANAGE"]

    def __init__(self, client: ApiClient):
        super().__init__(client, "2.0/preview/permissions/authorization/tokens", "token")

    @property
    def permission_levels(self):
        response = self.client.execute_get_json(f"{self.path}/permissionLevels")
        return response.get("permission_levels", [])

    def update(self, object_id: str, what: What, value: str, permission_level: PermissionLevel):
        self._validate_what(what)
        self._validate_permission_level(permission_level)
        acl = [
                {
                    what: value,
                    "permission_level": permission_level
                }
            ]
        return self.client.api_simple("PUT", f"{self.path}", access_control_list=acl)
