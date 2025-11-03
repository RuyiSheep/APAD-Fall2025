# backend/app.py
# Minimal Flask API for the Project Service ONLY (MongoDB)

import os
from flask_cors import CORS
import projects_db as pdb
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()



app = Flask(__name__)
CORS(app)  # dev only
# --- Mongo connection ---
# Set MONGO_URI in your environment (or docker-compose):
# e.g. mongodb://localhost:27017
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

def get_client():
    # For Cosmos RU-based you may need tls=true&retrywrites=false in URI.
    return MongoClient(MONGO_URI, tlsAllowInvalidCertificates=True)

@app.get("/api/health")
def health():
    try:
        with get_client() as c:
            c.admin.command("ping")
        return {"ok": True}, 200
    except Exception as e:
        return {"ok": False, "error": str(e)}, 500

# --- Endpoints (Project only) ---

@app.post("/projects")
def create_project():
    data = request.get_json() or {}
    name = data.get("projectName")
    project_id = data.get("projectId")
    description = data.get("description", "")
    owner_user_id = data.get("ownerUserId") or data.get("owner_user_id")

    # minimal validation
    if not name or not project_id or not owner_user_id:
        return {"error": "projectName, projectId, ownerUserId are required"}, 400

    with get_client() as c:
        res = pdb.create_project(c, name, project_id, description)
        if res != "Project added successfully":
            return {"status": "failure", "message": res}, 409
        # add owner as first member
        pdb.add_member(c, project_id, str(owner_user_id))

    return {
        "status": "success",
        "project": {
            "projectId": project_id,
            "projectName": name,
            "description": description,
            "ownerUserId": str(owner_user_id),
        }
    }, 201

@app.get("/projects/<project_id>")
def get_project(project_id):
    with get_client() as c:
        ok, result = pdb.get_project(c, project_id)
        if not ok:
            return {"message": result}, 404
        # shape the response cleanly
        return {
            "projectId": result.get("projectId"),
            "projectName": result.get("projectName"),
            "description": result.get("description") or "",
            "users": result.get("users") or [],
            "hwSets": result.get("hwSets") or {},
        }, 200

@app.post("/projects/<project_id>/members")
def add_member(project_id):
    data = request.get_json() or {}
    user_id = data.get("userId") or data.get("user_id")
    if not user_id:
        return {"error": "userId is required"}, 400

    with get_client() as c:
        msg = pdb.add_member(c, project_id, str(user_id))
        if msg == "Project does not exist":
            return {"error": msg}, 404
        if msg == "Project already joined":
            return {"error": msg}, 409
        return {"ok": True, "message": msg}, 201

if __name__ == "__main__":
    from os import getenv
    port = int(os.getenv("PORT", "5002"))
    app.run(host="0.0.0.0", port=port, debug=False)
