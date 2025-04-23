from models.rbac_model import Permission, Role, RolePermission
from models.user_model import User
from repositories.rbac_repository import RbacRepository
from schemas.rbac_schema import PutPermissionSchemaRequest


class RbacService:
    def __init__(self, rbac_repository: RbacRepository): 
        self.rbac_repository = rbac_repository

    def get_all_roles_with_permissions(self) -> list[Role]:
        return self.rbac_repository.get_all_roles_with_permissions()
    
    def get_role_by_id(self, role_id: int) -> Role | None:
        return self.rbac_repository.get_role_by_id(role_id)
    
    def get_role_by_name(self, role_name: str) -> Role | None:
        return self.rbac_repository.get_role_by_name(role_name)
    
    def get_or_put_role(self, role_name: str) -> Role | None:
        role = self.rbac_repository.get_role_by_name(role_name)
        if not role:
            role = Role(name=role_name)
            self.rbac_repository.commit_and_refresh(role)
        return role
    
    def get_all_permissions(self) -> list[Permission]:
        return self.rbac_repository.get_all_permissions()
    
    def get_permission_by_id(self, permission_id: int) -> Permission | None:
        return self.rbac_repository.get_permission_by_id(permission_id)
    
    def get_or_put_permission(self, permission_name: str, user: User) -> Permission | None:
        permission = self.rbac_repository.get_permissions_by_name([permission_name])
        if not permission:
            permission = Permission(name=permission_name, created_by_id=user.id)
            self.rbac_repository.commit_and_refresh(permission)
        return permission
    
    def update_permission(
        self, 
        permission: Permission, 
        updated_permission: PutPermissionSchemaRequest,
        user: User
    ) -> Permission | None:
        permission.name = updated_permission.name
        permission.created_by_id = user.id
        self.rbac_repository.commit_and_refresh(permission)
        return permission

    def delete_permission(self, permission: Permission):
        self.rbac_repository.delete(permission)

    def update_role_permissions(self, role: Role, permissions: list[str], user: User) -> Role | None:
        role.role_permissions.clear()
        permissions = self.rbac_repository.get_permissions_by_name(permissions)
        for permission in permissions:
            role_permission = RolePermission(
                role_id=role.id,
                permission_id=permission.id,
                created_by_id=user.id
            )
            role.role_permissions.append(role_permission)

        self.rbac_repository.commit_and_refresh(role)
        return role