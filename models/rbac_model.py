import enum
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime, Enum as SqlEnum, Table, func
from sqlalchemy.orm import relationship

from models.base_model import Base


class RoleEnum(enum.Enum):
    ADMIN = "admin"
    USERADMIN = "useradmin"
    USERREAD = "userread"
    RBACADMIN = "rbacadmin"
    SWAPIREAD = "swapiread"

class PermissionEnum(enum.Enum):
    SWAPIREAD = "swapi:read"
    USERREAD = "user:read"
    USERDELETE = "user:delete"
    USERWRITE = "user:write"
    RBACREAD = "rbac:read"
    RBACWRITE = "rbac:write"
    RBACDELETE = "rbac:delete"
    RBACADMIN = "rbac:admin"

class Role(Base):
    __tablename__ = 'roles'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(
        SqlEnum(RoleEnum, native_enum=False, values_callable=lambda obj: [e.value for e in obj]),
        unique=True,
        nullable=False
    )

    # Relationships
    role_permissions = relationship("RolePermission", back_populates="role", cascade="all, delete-orphan")


user_roles = Table(
    'user_roles',
    Base.metadata,
    Column('user_id', ForeignKey('users.id'), primary_key=True),
    Column('role_id', ForeignKey('roles.id'), primary_key=True),
)

# Permission model
class Permission(Base):
    __tablename__ = 'permissions'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by_id = Column(ForeignKey('users.id'), nullable=False)

    role_permissions = relationship(
        "RolePermission",
        back_populates="permission",
        cascade="all, delete-orphan"
    )
    

# Join table as a class
class RolePermission(Base):
    __tablename__ = 'role_permissions'
    role_id = Column(ForeignKey('roles.id'), primary_key=True)
    permission_id = Column(ForeignKey('permissions.id'), primary_key=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    created_by_id = Column(ForeignKey('users.id'), nullable=False)

    # Relationships
    role = relationship("Role", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
    
    