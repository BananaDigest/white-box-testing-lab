def update_task_status(task, new_status, user_role):
    valid_transitions = {
        "open": ["in_progress", "closed"],
        "in_progress": ["closed", "on_hold"],
        "on_hold": ["in_progress"],
        "closed": []
    }
    if task["status"] == new_status:
        return "No change"
    if new_status not in valid_transitions.get(task["status"], []):
        return "Invalid transition"
    if user_role not in ["admin", "manager"] and new_status == "closed":
        return "Permission denied"
    task["status"] = new_status
    return "Updated"
