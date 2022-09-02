from dbacademy.dbrest import DBAcademyRestClient
from dbacademy.rest.common import ApiContainer

__all__ = ["Tokens"]

# noinspection PyProtectedMember
from dbacademy.rest.permissions.crud import What, PermissionLevel

class Tokens(ApiContainer):
    def __init__(self, client: DBAcademyRestClient):
        self.client = client
        self.base_url = f"{self.client.endpoint}/permissions/authorization/tokens"

    def get_levels(self) -> dict:
        return self.client.execute_get_json(f"{self.base_url}/permissionLevels")

    # def update(self, object_id: str, what: What, value: str, permission_level: PermissionLevel):
    #     self._validate_what(what)
    #     self._validate_permission_level(permission_level)
    #     acl = [
    #             {
    #                 what: value,
    #                 "permission_level": permission_level
    #             }
    #         ]
    #     return self.client.api_simple("PATCH", f"{self.path}", access_control_list=acl)
