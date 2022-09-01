from dbacademy.rest.common import ApiClient
from dbacademy.rest.permissions.crud import PermissionsCrud

__all__ = ["Jobs"]


class Jobs(PermissionsCrud):
    valid_permissions = ["IS_OWNER", "CAN_MANAGE_RUN", "CAN_VIEW", "CAN_MANAGE"]

    def __init__(self, client: ApiClient):
        super().__init__(client, "2.0/preview/permissions/jobs", "job")
