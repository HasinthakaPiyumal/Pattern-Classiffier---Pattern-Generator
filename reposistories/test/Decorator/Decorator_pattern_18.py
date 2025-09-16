def require_role(required_role):
    def decorator(func):
        def wrapper(user_role, *args, **kwargs):
            if user_role == required_role:
                print(f"Access granted for user with role '{user_role}'.")
                return func(user_role, *args, **kwargs)
            else:
                print(f"Access denied! Role '{user_role}' is not '{required_role}'.")
                return None
        return wrapper
    return decorator

@require_role("admin")
def delete_data(user_role, item_id):
    return f"Data item {item_id} deleted by {user_role}."

@require_role("user")
def view_profile(user_role, user_id):
    return f"Profile {user_id} viewed by {user_role}."

if __name__ == '__main__':
    print(delete_data("admin", 123))
    print(delete_data("user", 456))
    print(view_profile("user", 789))
    print(view_profile("admin", 000))