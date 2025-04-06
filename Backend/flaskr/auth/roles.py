# constants to verify user roles from JWT

JWT_ROLE_ADMIN = "admin"
JWT_ROLE_USER = "user"

def has_admin_rights(role):
    """
    has_admin_rights returns whether the token bearer
    is allowed to access a ressource which only the users 
    in the admin domain are allowed to access
    """
    return role == JWT_ROLE_ADMIN

def has_user_rights(role):
    """
    has_user_rights returns whether the token bearer
    is allowed to access a ressource which only the users
    in the user domain are allowed to access
    """
    return role == JWT_ROLE_USER or has_admin_rights(role)