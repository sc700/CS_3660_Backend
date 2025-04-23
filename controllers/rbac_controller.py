from fastapi import APIRouter, Depends, HTTPException, status, Request
from dependency_injector.wiring import Provide, inject

from containers import Container
from models.rbac_model import PermissionEnum
from schemas.message_schema import MessageResponse
from schemas.rbac_schema import PermissionSchema, PutNewRoleSchemaRequest, PutPermissionSchemaRequest, PutRoleSchemaRequest, RoleSchema
from services.auth_service import AuthorizationService
from services.rbac_service import RbacService

router = APIRouter(prefix="/api/rbac", tags=["Authorization", "RBAC"])

@router.delete("/permissions/{permission_id}", response_model=MessageResponse)
@inject
def delete_permission(request: Request,
                      permission_id: int,
                      rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                      auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN])

    permission = rbac_service.get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=404, detail="Permission not found")

    rbac_service.delete_permission(permission)
    return {"message": "Permission deleted successfully"}

@router.get("/permissions/{permission_id}", response_model=PermissionSchema)
@inject
def get_permission(request: Request,
                   permission_id: int,
                   rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                   auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACREAD])

    permission = rbac_service.get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    return permission

@router.put("/permissions/{permission_id}", response_model=PermissionSchema)
@inject
def put_permission(request: Request,
                   permission_id: int,
                   updated_permission: PutPermissionSchemaRequest,
                   rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                   auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACWRITE])

    permission = rbac_service.get_permission_by_id(permission_id)
    if not permission:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")

    rbac_service.update_permission(permission, updated_permission, auth_service.user)
    return permission

@router.get("/permissions", response_model=list[PermissionSchema])
@inject
def get_permissions(request: Request,
                    rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                    auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACREAD])
    return rbac_service.get_all_permissions()

@router.put("/permissions", response_model=PermissionSchema)
@inject
def put_permission_create(request: Request,
                          permission: PutPermissionSchemaRequest,
                          rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                          auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACWRITE])
    return rbac_service.get_or_put_permission(permission.name, auth_service.user)

@router.get("/roles", response_model=list[RoleSchema])
@inject
def get_roles(request: Request,
              rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
              auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACREAD])
    return rbac_service.get_all_roles_with_permissions()

@router.put("/roles", response_model=RoleSchema)
@inject
def put_roles(request: Request,
              role_request: PutNewRoleSchemaRequest,
              rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
              auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACWRITE])

    role = rbac_service.get_or_put_role(role_request.name)
    if not role:
        raise HTTPException(status_code=400, detail="Failed to create role")

    return role

@router.get("/roles/{role_id}", response_model=RoleSchema)
@inject
def get_role(request: Request,
             role_id: int,
             rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
             auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACREAD])

    role = rbac_service.get_role_by_id(role_id)
    if not role:
        return {"message": "Role not found"}
    return role

@router.put("/roles/{role_id}/permissions", response_model=RoleSchema)
@inject
def update_role_permissions(request: Request,
                            role_id: int,
                            permissions: PutRoleSchemaRequest,
                            rbac_service: RbacService = Depends(Provide[Container.rbac_service]),
                            auth_service: AuthorizationService = Depends(Provide[Container.auth_service])):
    auth_service.assert_permissions(request, [PermissionEnum.RBACADMIN, PermissionEnum.RBACWRITE])

    role = rbac_service.get_role_by_id(role_id)
    if not role:
        raise HTTPException(status_code=404, detail="Role not found")

    role = rbac_service.update_role_permissions(role, permissions.role_permissions, auth_service.user)
    if not role:
        return {"message": "Failed to update role permissions"}

    return role
