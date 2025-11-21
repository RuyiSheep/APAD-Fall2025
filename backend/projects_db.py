from typing import Tuple, Dict, Any
from pymongo.collection import Collection

# Collection helper
def projects_col(client) -> Collection:
    return client["ProjectService"]["projects"]

# Schema we will use going forward:
# {
#   "projectId": str (unique),
#   "projectName": str,
#   "description": str,
#   "users": [str, ...],          # list of user IDs (opaque strings)
#   "hwSets": { str: int, ... }   # usage, kept for future; starts empty
# }

def get_project(client, project_id: str) -> Tuple[bool, Any]:
    col = projects_col(client)
    doc = col.find_one({"projectId": project_id})
    if not doc:
        return False, "Project does not exist"
    return True, doc

def create_project(client, project_name: str, project_id: str, description: str) -> str:
    col = projects_col(client)
    if col.find_one({"projectId": project_id}):
        return "ProjectId already taken"
    doc = {
        "projectId": project_id,
        "projectName": project_name,
        "description": description or "",
        "users": [],          # owner will be added by the service
        "hwSets": {}          # keep structure consistent with future needs
    }
    col.insert_one(doc)
    return "Project added successfully"

def add_member(client, project_id: str, user_id: str) -> str:
    col = projects_col(client)
    proj = col.find_one({"projectId": project_id})
    if not proj:
        return "Project does not exist"
    # avoid duplicates
    if user_id in (proj.get("users") or []):
        return "Project already joined"
    col.update_one({"projectId": project_id}, {"$push": {"users": user_id}})
    return "Project joined successfully"

def update_hw_usage(client, project_id: str, hw_set_name: str, qty: int) -> Tuple[bool, str]:
    """
    Update hardware usage for a project.
    Args:
        client: MongoClient instance
        project_id: Project ID
        hw_set_name: Hardware set name (e.g., "HWSet1")
        qty: Quantity to add (positive for checkout, negative for checkin)
    Returns:
        Tuple[bool, str]: (success, message)
    """
    col = projects_col(client)
    proj = col.find_one({"projectId": project_id})
    if not proj:
        return False, "Project does not exist"
    
    # Get current hwSets or initialize empty dict
    hw_sets = proj.get("hwSets", {})
    current_qty = hw_sets.get(hw_set_name, 0)
    new_qty = current_qty + qty
    
    # Validate: can't have negative quantity
    if new_qty < 0:
        return False, "Cannot check in more than currently checked out"
    
    # Update hwSets
    if new_qty == 0:
        # Remove the key if quantity becomes zero
        hw_sets.pop(hw_set_name, None)
    else:
        hw_sets[hw_set_name] = new_qty
    
    # Update the project document
    col.update_one(
        {"projectId": project_id},
        {"$set": {"hwSets": hw_sets}}
    )
    
    return True, "Hardware usage updated successfully"
