def validate_input(user, password):
    if not user:
        return "Missing user"
    if len(password) < 8:
        return "Weak password"
    if any(char.isdigit() for char in password) and \
       any(char.isupper() for char in password):
        return "Valid"
    return "Invalid"
