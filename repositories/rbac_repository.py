from database.db import DatabaseFactory
from models.rbac_model import Permission, Role, RolePermission

from sqlalchemy.orm import Session, joinedload

class RbacRepository:
    def __init__(self, db: DatabaseFactory):
        self.db: Session = db.get_session()

    def get_all_roles_with_permissions(self) -> list[Role] | None:
        return ( 
            self.db.query(Role)
            .options(
                joinedload(Role.role_permissions)
                .joinedload(RolePermission.permission)
            )
            .all()
        )
    
    def get_role_by_id(self, role_id: int) -> Role | None:
        return (
            self.db.query(Role)
            .options(
                joinedload(Role.role_permissions)
                .joinedload(RolePermission.permission)
            )
            .filter(Role.id == role_id)
            .first()
        )
    
    def get_permissions_by_name(self, permissions: list[str]) -> list[Permission] | None:
        return (
            self.db.query(Permission)
            .filter(Permission.name.in_(permissions))
            .all()
        )
    
    def get_permission_by_id(self, permission_id: int) -> Permission | None:
        return (
            self.db.query(Permission)
            .filter(Permission.id == permission_id)
            .first()
        )
    
    def get_role_by_name(self, role_name: str) -> Role | None:
        return (
            self.db.query(Role)
            .options(
                joinedload(Role.role_permissions)
                .joinedload(RolePermission.permission)
            )
            .filter(Role.name == role_name)
            .first()
        )
    
    def get_only_role_by_name(self, role_name: str) -> Role | None:
        return (
            self.db.query(Role)            
            .filter(Role.name == role_name)
            .first()
        )

    def get_all_permissions(self) -> list[Permission] | None:
        return (
            self.db.query(Permission)
            .all()
        )
    
    def commit_and_refresh(self, instance):
        self.db.add(instance)
        self.db.commit()
        self.db.refresh(instance)

    def delete(self, instance):
        try:
            self.db.delete(instance)
            self.db.commit()
        except Exception as e:
            self.db.rollback()
            raise e