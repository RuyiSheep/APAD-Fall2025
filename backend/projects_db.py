from typing import Tuple, Dict, Any
from pymongo.collection import Collection

# Collection helper
def projects_col(client) -> Collection:
    return client["GitHard"]["projects"]

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
