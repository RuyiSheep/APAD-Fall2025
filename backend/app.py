# backend/app.py
# Flask API for the Project Service (MongoDB)

import os
from flask_cors import CORS
import projects_db as pdb
from flask import Flask, request, jsonify
from pymongo import MongoClient
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Mongo connection ---
# Set MONGO_URI in your environment (or docker-compose):
# Format: mongodb+srv://user:password@host.net/?appName=...
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

def get_client():
    """
    Get MongoDB client with proper SSL/TLS configuration for Docker environments.
    Matches the pattern used by hardware service for consistency.
    """
    # Check if we need to allow invalid certificates (for Docker/development environments)
    allow_invalid_certs_env = os.getenv('MONGO_ALLOW_INVALID_CERTS', 'true').lower()
    allow_invalid_certs = allow_invalid_certs_env == 'true'
    
    # Build connection string - add TLS parameters like hardware service
    connection_string = MONGO_URI
    is_srv = connection_string.startswith('mongodb+srv://')
    
    # Add tlsAllowInvalidCertificates to connection string if needed
    if allow_invalid_certs and is_srv:
        if '?' in connection_string:
            if 'tlsAllowInvalidCertificates' not in connection_string:
                connection_string += '&tlsAllowInvalidCertificates=true'
        else:
            connection_string += '?tlsAllowInvalidCertificates=true'
    
    client = MongoClient(
        connection_string,
        serverSelectionTimeoutMS=5000,
        connectTimeoutMS=10000,
        socketTimeoutMS=20000,
        tlsAllowInvalidCertificates=allow_invalid_certs,
        directConnection=False if is_srv else None
    )
    
    return client

@app.get("/")
@app.route("/", methods=['GET'])
def root():
    """Root endpoint"""
    return jsonify({"message": "Project Service API", "version": "1.0.0"})

@app.get("/api/health")
@app.route("/api/health", methods=['GET'])
def health():
    try:
        with get_client() as c:
            c.admin.command("ping")
        return {"ok": True}, 200
    except Exception as e:
        return {"ok": False, "error": str(e)}, 500

# --- Endpoints matching the original Flask app format ---

@app.route("/create_project", methods=['POST'])
def create_project():
    """
    Create a new project.
    Matches the original Flask app endpoint format.
    """
    data = request.get_json() or {}
    name = data.get("projectName")
    project_id = data.get("projectId")
    description = data.get("description", "")
    user_id = data.get("userId")

    # minimal validation
    if not name or not project_id:
        return jsonify({"status": "failure", "message": "projectName and projectId are required"}), 400

    with get_client() as c:
        res = pdb.create_project(c, name, project_id, description)
        if res != "Project added successfully":
            return jsonify({"status": "failure", "message": res}), 409
        
        # Add creator as first member if userId provided
        if user_id:
            pdb.add_member(c, project_id, str(user_id))

    return jsonify({
        "status": "success",
        "message": "Project added successfully"
    }), 200

@app.route("/get_project_info", methods=['GET'])
def get_project_info():
    """
    Get project information.
    Matches the original Flask app endpoint format.
    """
    project_id = request.args.get("projectId")
    
    if not project_id:
        return jsonify({"error": "Missing 'projectId' in request"}), 400

    with get_client() as c:
        ok, result = pdb.get_project(c, project_id)
        if not ok:
            return jsonify({"message": result}), 404
        
        # Shape the response to match original Flask app format
        return jsonify({
            "projectId": result.get("projectId"),
            "projectName": result.get("projectName"),
            "description": result.get("description") or "",
            "users": result.get("users") or [],
            "hwSets": result.get("hwSets") or {}
        }), 200

@app.route("/join_project", methods=['POST'])
def join_project():
    """
    Join a project.
    Matches the original Flask app endpoint format.
    """
    data = request.get_json() or {}
    project_id = data.get("projectId")
    user_id = data.get("userId")
    
    if not project_id or not user_id:
        return jsonify({"status": "failure", "message": "projectId and userId are required"}), 400

    with get_client() as c:
        # Check if project exists
        ok, project = pdb.get_project(c, project_id)
        if not ok:
            return jsonify({"status": "failure", "message": "Project does not exist"}), 404
        
        # Add member
        msg = pdb.add_member(c, project_id, str(user_id))
        if msg == "Project does not exist":
            return jsonify({"status": "failure", "message": msg}), 404
        if msg == "Project already joined":
            return jsonify({"status": "failure", "message": msg}), 409
        
        return jsonify({"status": "success", "message": "Project joined successfully"}), 200

@app.route("/update_hw_usage", methods=['POST'])
def update_hw_usage():
    """
    Update hardware usage for a project (called after checkout/checkin).
    This keeps the project's hwSets field in sync with hardware checkouts.
    """
    data = request.get_json() or {}
    project_id = data.get("projectId")
    hw_set_name = data.get("hwSetName")
    qty = data.get("qty")
    
    if not project_id or not hw_set_name or qty is None:
        return jsonify({"status": "failure", "message": "projectId, hwSetName, and qty are required"}), 400
    
    try:
        qty = int(qty)
    except (ValueError, TypeError):
        return jsonify({"status": "failure", "message": "qty must be an integer"}), 400

    with get_client() as c:
        success, message = pdb.update_hw_usage(c, project_id, hw_set_name, qty)
        if not success:
            return jsonify({"status": "failure", "message": message}), 400
        
        return jsonify({"status": "success", "message": message}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", "5003"))
    app.run(host="0.0.0.0", port=port, debug=False)
