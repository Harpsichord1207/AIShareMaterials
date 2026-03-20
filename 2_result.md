# API Design: Task Management System

## Base URL

```
https://api.taskmanager.com/v1
```

## Authentication

All protected endpoints require:
```
Authorization: Bearer <jwt_token>
```

---

## Endpoints

### Authentication

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/register` | Register new user |
| POST | `/auth/login` | Login and get JWT |
| POST | `/auth/refresh` | Refresh access token |
| POST | `/auth/logout` | Invalidate token |

### Users

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/me` | Get current user profile |
| PATCH | `/users/me` | Update profile |
| DELETE | `/users/me` | Delete account |

### Tasks

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/tasks` | List all tasks (paginated) |
| POST | `/tasks` | Create new task |
| GET | `/tasks/:id` | Get task details |
| PATCH | `/tasks/:id` | Update task |
| DELETE | `/tasks/:id` | Delete task |
| POST | `/tasks/:id/assign` | Assign task to user |

### Categories

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/categories` | List all categories |
| POST | `/categories` | Create category |
| DELETE | `/categories/:id` | Delete category |

---

## Request/Response Examples

### Register User

```json
// POST /auth/register
// Request
{
  "email": "user@example.com",
  "password": "SecurePass123!",
  "name": "John Doe"
}

// Response 201
{
  "success": true,
  "data": {
    "user": {
      "id": "usr_abc123",
      "email": "user@example.com",
      "name": "John Doe",
      "created_at": "2026-03-20T10:30:00Z"
    },
    "tokens": {
      "access_token": "eyJhbGciOiJIUzI1NiIs...",
      "refresh_token": "eyJhbGciOiJIUzI1NiIs...",
      "expires_in": 3600
    }
  }
}
```

### Create Task

```json
// POST /tasks
// Request
{
  "title": "Complete API documentation",
  "description": "Write comprehensive docs for all endpoints",
  "priority": "high",
  "due_date": "2026-03-25T18:00:00Z",
  "category_ids": ["cat_work", "cat_urgent"]
}

// Response 201
{
  "success": true,
  "data": {
    "id": "task_xyz789",
    "title": "Complete API documentation",
    "description": "Write comprehensive docs for all endpoints",
    "priority": "high",
    "status": "pending",
    "due_date": "2026-03-25T18:00:00Z",
    "categories": [
      {"id": "cat_work", "name": "Work"},
      {"id": "cat_urgent", "name": "Urgent"}
    ],
    "created_at": "2026-03-20T10:35:00Z",
    "updated_at": "2026-03-20T10:35:00Z"
  }
}
```

---

## Error Response Format

```json
{
  "success": false,
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid input data",
    "details": [
      {
        "field": "email",
        "message": "Must be a valid email address"
      }
    ]
  }
}
```

### Error Codes

| Code | HTTP Status | Description |
|------|-------------|-------------|
| `UNAUTHORIZED` | 401 | Missing or invalid token |
| `FORBIDDEN` | 403 | Insufficient permissions |
| `NOT_FOUND` | 404 | Resource not found |
| `VALIDATION_ERROR` | 400 | Invalid request data |
| `CONFLICT` | 409 | Resource already exists |
