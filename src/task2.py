def check_access(role, is_active, is_admin):
    if (role == "user" and is_active) or is_admin:
        return True
    return False
