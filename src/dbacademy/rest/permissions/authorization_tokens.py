from dbacademy.rest.common import ApiClient
from dbacademy.rest.permissions.crud import PermissionsCrud

__all__ = ["Tokens"]


class Tokens(PermissionsCrud):

    def __init__(self, client: ApiClient):
        super().__init__(client, "2.0/permissions/authorization/tokens", "token")

    @property
    def permission_levels(self):
        response = self.client.execute_get_json(f"{self.path}/permissionLevels")
        return response #.get("permission_levels", [])
