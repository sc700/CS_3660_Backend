from operator import attrgetter
from cachetools import TTLCache, cachedmethod
from fastapi import HTTPException
from cachetools.keys import hashkey

from models.user_model import User
from repositories.user_repository import UserRepository


class AuthorizationService:
    _cache = TTLCache(maxsize=100, ttl=60)  # Cache for 1 minute
    
    def __init__(self, user_repository, logger):
        self.user_repository: UserRepository = user_repository
        self.logger = logger

    def assert_permissions(self, request, permissions):
        if not request.state.jwt_payload:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        self.user = self.user_repository.get_user_by_username(request.state.jwt_payload["user"]["username"])
        if not self.user:
            raise HTTPException(status_code=403, detail="Forbidden")

        # for possible caching later
        user_permissions = self._get_user_permissions(self.user)
        
        # check if user has at least one of the permissions
        if any(permission.value in user_permissions for permission in permissions):
            return
                
        raise HTTPException(status_code=403, detail="Forbidden")

    @cachedmethod(attrgetter('_cache'), key=lambda self, user: hashkey(user.username))
    def _get_user_permissions(self, user: User):
        # sanity check
        if not user:
            raise HTTPException(status_code=403, detail="Forbidden")

        self.logger.debug(f"Cache permissions miss for {user.username}: Fetching permissions from DB")        
        
        # get all permissions for the user
        permissions = set()
        for role in user.roles:
            for permission in role.role_permissions:
                permissions.add(permission.permission.name)
        
        return permissions
    
    def assert_roles(self, request, roles):
        if not request.state.jwt_payload:
            raise HTTPException(status_code=403, detail="Forbidden")
        
        user = self.user_repository.get_user_by_username(request.state.jwt_payload["user"]["username"])
        if not user:
            raise HTTPException(status_code=403, detail="Forbidden")

        # check if user has at least one of the roles
        if any(user.has_role(role) for role in roles):
            return            
        
        raise HTTPException(status_code=403, detail="Forbidden")
