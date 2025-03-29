# constants to verify user roles from JWT

JWT_ROLE_GROUP = "group"
JWT_ROLE_ADMIN = "admin"
JWT_ROLE_LOCATION = "location"
JWT_ROLE_USER = "user"

def has_admin_rights(role):
    """
    has_admin_rights returns whether the token bearer
    is allowed to access a ressource which only the users 
    in the admin domain are allowed to access
    """
    return role == JWT_ROLE_ADMIN

def has_location_rights(role):
    """
    has_location_rights returns whether the token bearer
    is allowed to access a ressource which only the users
    in the location domain are allowed to access

    this also includes the admins
    """
    return role == JWT_ROLE_LOCATION or has_admin_rights(role)

def has_group_rights(role):
    """
    has_group_rights returns whether the token bearer
    is allowed to access a ressource which only the users
    in the location domain are allowed to access

    this also includes the admins and location
    """
    return role == JWT_ROLE_GROUP or has_location_rights(role) or has_admin_rights(role)
