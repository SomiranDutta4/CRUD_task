# CRUD Task Management API

A FastAPI-based task management system with role-based access control using MongoDB Atlas.

## Features

* User Registration
* User Authentication
* Admin Registration
* Admin Authentication
* Manager Assignment
* Task Creation
* Task Updates
* View Own Tasks
* Managers Can View Assigned Employees' Tasks

---

## Tech Stack

* FastAPI
* MongoDB Atlas
* Motor (Async MongoDB Driver)
* Pydantic
* bcrypt
* Python 3

---

## Project Structure

```text
app/
│
├── database/
│   └── db.py
│
├── routes/
│   ├── user_route.py
│   ├── task_route.py
│   └── admin.py
│
├── schemas/
│   ├── user_schema.py
│   ├── task_schema.py
│   └── admin_schema.py
│
├── services/
│   ├── hash.py
│   └── checkAdmin.py
│
└── main.py
```

---

## Installation

Clone the repository:

```bash
git clone <your-repository-url>
cd CRUD_task
```

Create and activate virtual environment:

```bash
python -m venv venv

# Linux / macOS
source venv/bin/activate

# Windows
venv\Scripts\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## Environment Variables

Create a `.env` file in the project root:

```env
MONGO_URL=your_mongodb_connection_string
secret_key=your_admin_secret_key
```

---

## Run Server

```bash
uvicorn app.main:app --reload
```

Server will start on:

```text
http://127.0.0.1:8000
```

---

## API Documentation

Swagger UI:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# API Endpoints

## User Routes

### User Signup

```http
POST /user/signup
```

Request Body:

```json
{
  "username": "john",
  "email": "john@example.com",
  "password": "password123"
}
```

---

### User Signin

```http
POST /user/signin
```

Request Body:

```json
{
  "email": "john@example.com",
  "password": "password123"
}
```

---

## Admin Routes

### Admin Signup

```http
POST /admin/signup
```

Request Body:

```json
{
  "username": "admin",
  "email": "admin@example.com",
  "password": "password123",
  "admin_key": "your-secret-key"
}
```

---

### Admin Signin

```http
POST /admin/signin
```

Request Body:

```json
{
  "email": "admin@example.com",
  "password": "password123"
}
```

---

### Assign Manager

```http
PUT /admin/manager/update
```

Query Parameters:

```text
admin_id=<admin-id>
```

Request Body:

```json
{
  "employee_id": "employee-id",
  "manager_id": "manager-id"
}
```

---

## Task Routes

### Get Tasks

```http
GET /task/
```

Query Parameters:

```text
user_id=<user-id>
```

Returns:

* User's own tasks
* Tasks assigned to employees managed by the user

---

### Create Task

```http
POST /task/
```

Query Parameters:

```text
user_id=<creator-id>
target_user=<target-user-id>
```

Request Body:

```json
{
  "title": "Finish Assignment",
  "description": "Complete FastAPI CRUD project"
}
```

---

### Update Task

```http
PUT /task/{task_id}
```

Query Parameters:

```text
user_id=<user-id>
```

Request Body:

```json
{
  "title": "Updated Task",
  "description": "Updated Description",
  "completed": true
}
```

---

## Database Design

### Users Collection

```json
{
  "_id": "ObjectId",
  "username": "john",
  "email": "john@example.com",
  "hashed_password": "...",
  "is_admin": false,
  "manager_id": null
}
```

---

### Tasks Collection

```json
{
  "_id": "ObjectId",
  "title": "Task Title",
  "description": "Task Description",
  "completed": false,
  "isUpdated": false,
  "user_id": "user-id",
  "self_task": true
}
```

---

## Future Improvements

* JWT Authentication
* Role-Based Authorization Middleware
* Task Deletion
* User Deletion
* Pagination
* Task Filtering
* Unit Testing
* Docker Support

---

## Author

Somiran Dutta
