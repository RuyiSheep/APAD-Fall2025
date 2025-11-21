# Project Service Microservice

A standalone Flask microservice for managing projects. This service is part of the githard microservices architecture.

## Features

- Project creation
- Project information retrieval
- Project member management (join project)
- Automatic API documentation
- Docker containerization support

## Architecture

- **Framework**: Flask
- **Database**: MongoDB (separate `ProjectService` database)
- **Port**: 5003
- **API Gateway**: Routes requests from `githard-frontend`

## Prerequisites

- Python 3.12+
- MongoDB (or use MongoDB container from docker-compose)

## Setup

### Local Development

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create `.env` file:
```env
MONGO_URI=mongodb+srv://user:password@host.net/ProjectService?retryWrites=true&w=majority
PORT=5003
```

4. Run the service:
```bash
python app.py
```

## API Endpoints

### POST `/create_project`
Create a new project.

**Request Body:**
```json
{
  "userId": "user123",
  "projectName": "My Project",
  "projectId": "project123",
  "description": "Project description"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Project added successfully"
}
```

### GET `/get_project_info`
Get project information.

**Query Parameters:**
- `projectId` (string, required): The project ID

**Response:**
```json
{
  "projectId": "project123",
  "projectName": "My Project",
  "description": "Project description",
  "users": ["user123"],
  "hwSets": {}
}
```

### POST `/join_project`
Join an existing project.

**Request Body:**
```json
{
  "userId": "user123",
  "projectId": "project123"
}
```

**Response:**
```json
{
  "status": "success",
  "message": "Project joined successfully"
}
```

## Database Schema

### Projects Collection (`projects`)
```json
{
  "projectId": "project123",
  "projectName": "My Project",
  "description": "Project description",
  "users": ["user123", "user456"],
  "hwSets": {
    "HWSet1": 10,
    "HWSet2": 5
  }
}
```

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGO_URI` | Full MongoDB connection string | Required |
| `PORT` | Service port | `5003` |

## Notes

- This service maintains project membership and hardware usage tracking
- Hardware checkout/check-in operations are handled by the hardware service
- User project lists are maintained by the user service
- The API Gateway coordinates between services for operations that require multiple services
