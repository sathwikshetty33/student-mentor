# Mentor-Student Platform API Documentation

## Table of Contents
1. [Overview](#overview)
2. [Authentication](#authentication)
3. [Base URL](#base-url)
4. [API Endpoints](#api-endpoints)
   - [Authentication Endpoints](#authentication-endpoints)
   - [Student Profile Endpoints](#student-profile-endpoints)
   - [Mentor Profile Endpoints](#mentor-profile-endpoints)
   - [Test Management Endpoints](#test-management-endpoints)
   - [Test Score Management Endpoints](#test-score-management-endpoints)
5. [Error Responses](#error-responses)
6. [Testing Guide](#testing-guide)

## Overview

This API provides endpoints for a mentor-student platform where:
- **Students** can register, login, and manage their profiles
- **Mentors** can register, login, manage profiles, create tests, and assign scores
- **Authentication** is handled via Django REST Framework Token Authentication
- **Permissions** are role-based (Student vs Mentor)

## Authentication

This API uses **Token Authentication**. After successful login or registration, you'll receive a token that must be included in the Authorization header for protected endpoints.

### Header Format:
```
Authorization: Token <your_token_here>
```

## Base URL

```
http://localhost:8000/portal/
```

## API Endpoints

### Authentication Endpoints

#### 1. Student Registration
**Endpoint:** `POST /portal/register/student/`

**Description:** Register a new student account

**Headers:**
```
Content-Type: application/json
```

**Payload:**
```json
{
    "username": "string (required)",
    "email": "string (required)",
    "password": "string (required, min 6 chars)",
    "first_name": "string (optional)",
    "last_name": "string (optional)",
    "leetcode": "string (required)",
    "github": "string (required)",
    "photo": "string (optional)",
    "bio": "string (optional)"
}
```

**Example Request:**
```json
{
    "username": "alice_student",
    "email": "alice@example.com",
    "password": "securepass123",
    "first_name": "Alice",
    "last_name": "Johnson",
    "leetcode": "alice_leetcode",
    "github": "alice_github",
    "bio": "Computer science student interested in web development"
}
```

**Success Response (201):**
```json
{
    "message": "Student registered successfully",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "student_id": 1,
    "username": "alice_student"
}
```

---

#### 2. Mentor Registration
**Endpoint:** `POST /portal/register/mentor/`

**Description:** Register a new mentor account

**Headers:**
```
Content-Type: application/json
```

**Payload:**
```json
{
    "username": "string (required)",
    "email": "string (required)",
    "password": "string (required, min 6 chars)",
    "first_name": "string (optional)",
    "last_name": "string (optional)",
    "expertise": "string (required)",
    "github": "string (required)",
    "photo": "string (optional)",
    "bio": "string (optional)"
}
```

**Example Request:**
```json
{
    "username": "dr_smith",
    "email": "smith@example.com",
    "password": "mentorpass123",
    "first_name": "John",
    "last_name": "Smith",
    "expertise": "Full Stack Development",
    "github": "drsmith_dev",
    "bio": "Senior software engineer with 8 years experience"
}
```

**Success Response (201):**
```json
{
    "message": "Mentor registered successfully",
    "token": "8844b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 2,
    "mentor_id": 1,
    "username": "dr_smith"
}
```

---

#### 3. Login (Both Student and Mentor)
**Endpoint:** `POST /portal/login/`

**Description:** Login for both students and mentors

**Headers:**
```
Content-Type: application/json
```

**Payload:**
```json
{
    "username": "string (required)",
    "password": "string (required)"
}
```

**Example Request:**
```json
{
    "username": "alice_student",
    "password": "securepass123"
}
```

**Success Response (200):**
```json
{
    "message": "Login successful",
    "token": "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b",
    "user_id": 1,
    "user_type": "student",
    "profile_id": 1,
    "username": "alice_student"
}
```

---

### Student Profile Endpoints

#### 4. Get Own Student Profile
**Endpoint:** `GET /portal/profile/student/`

**Description:** Get current student's profile with test scores

**Headers:**
```
Authorization: Token <student_token>
```

**Payload:** None (GET request)

**Success Response (200):**
```json
{
    "id": 1,
    "user": {
        "id": 1,
        "username": "alice_student",
        "email": "alice@example.com",
        "first_name": "Alice",
        "last_name": "Johnson"
    },
    "leetcode": "alice_leetcode",
    "github": "alice_github",
    "dateJoined": "2024-08-03T10:30:00.000Z",
    "photo": null,
    "bio": "CS student",
    "test_scores": [
        {
            "id": 1,
            "test": {
                "id": 1,
                "name": "Python Basics",
                "description": "Basic Python programming concepts",
                "created_at": "2024-08-01T09:00:00.000Z",
                "updated_at": "2024-08-01T09:00:00.000Z"
            },
            "score": 85,
            "date_taken": "2024-08-03T11:00:00.000Z"
        }
    ]
}
```

---

#### 5. Get Specific Student Profile
**Endpoint:** `GET /portal/profile/student/<int:student_id>/`

**Description:** Get specific student's profile (accessible by the student themselves or any mentor)

**Headers:**
```
Authorization: Token <student_token_or_mentor_token>
```

**Payload:** None (GET request)

**Access:** Student (own profile only) or Mentor (any student)

**Success Response (200):** Same as above

---

#### 6. Update Student Profile
**Endpoint:** `PUT /portal/profile/student/` or `PUT /portal/profile/student/<int:student_id>/`

**Description:** Update student profile (student can only update own profile)

**Headers:**
```
Authorization: Token <student_token>
Content-Type: application/json
```

**Payload:**
```json
{
    "first_name": "string (optional)",
    "last_name": "string (optional)",
    "email": "string (optional)",
    "leetcode": "string (optional)",
    "github": "string (optional)",
    "photo": "string (optional)",
    "bio": "string (optional)"
}
```

**Example Request:**
```json
{
    "first_name": "Alice Updated",
    "bio": "Updated bio - Senior CS student specializing in AI",
    "leetcode": "alice_new_leetcode"
}
```

**Success Response (200):**
```json
{
    "message": "Profile updated successfully",
    "data": {
        "id": 1,
        "user": {
            "id": 1,
            "username": "alice_student",
            "email": "alice@example.com",
            "first_name": "Alice Updated",
            "last_name": "Johnson"
        },
        "leetcode": "alice_new_leetcode",
        "github": "alice_github",
        "dateJoined": "2024-08-03T10:30:00.000Z",
        "photo": null,
        "bio": "Updated bio - Senior CS student specializing in AI",
        "test_scores": []
    }
}
```

---

#### 7. Get All Students (Mentor Only)
**Endpoint:** `GET /portal/students/`

**Description:** Get list of all students (mentor access only)

**Headers:**
```
Authorization: Token <mentor_token>
```

**Payload:** None (GET request)

**Access:** Mentors only

**Success Response (200):**
```json
[
    {
        "id": 1,
        "user": {
            "id": 1,
            "username": "alice_student",
            "email": "alice@example.com",
            "first_name": "Alice",
            "last_name": "Johnson"
        },
        "leetcode": "alice_leetcode",
        "github": "alice_github",
        "dateJoined": "2024-08-03T10:30:00.000Z",
        "photo": null,
        "bio": "CS student",
        "test_scores": [...]
    }
]
```

---

### Mentor Profile Endpoints

#### 8. Get Mentor Profile
**Endpoint:** `GET /portal/profile/mentor/`

**Description:** Get current mentor's profile

**Headers:**
```
Authorization: Token <mentor_token>
```

**Payload:** None (GET request)

**Success Response (200):**
```json
{
    "id": 1,
    "user": {
        "id": 2,
        "username": "dr_smith",
        "email": "smith@example.com",
        "first_name": "John",
        "last_name": "Smith"
    },
    "expertise": "Full Stack Development",
    "github": "drsmith_dev",
    "dateJoined": "2024-08-03T10:45:00.000Z",
    "photo": null,
    "bio": "Senior software engineer with 8 years experience"
}
```

---

#### 9. Update Mentor Profile
**Endpoint:** `PUT /portal/profile/mentor/`

**Description:** Update mentor profile

**Headers:**
```
Authorization: Token <mentor_token>
Content-Type: application/json
```

**Payload:**
```json
{
    "first_name": "string (optional)",
    "last_name": "string (optional)",
    "email": "string (optional)",
    "expertise": "string (optional)",
    "github": "string (optional)",
    "photo": "string (optional)",
    "bio": "string (optional)"
}
```

**Example Request:**
```json
{
    "expertise": "Full Stack Development & DevOps",
    "bio": "Senior software engineer with 10 years experience",
    "first_name": "John Updated"
}
```

**Success Response (200):**
```json
{
    "message": "Profile updated successfully",
    "data": {
        "id": 1,
        "user": {
            "id": 2,
            "username": "dr_smith",
            "email": "smith@example.com",
            "first_name": "John Updated",
            "last_name": "Smith"
        },
        "expertise": "Full Stack Development & DevOps",
        "github": "drsmith_dev",
        "dateJoined": "2024-08-03T10:45:00.000Z",
        "photo": null,
        "bio": "Senior software engineer with 10 years experience"
    }
}
```

---

### Test Management Endpoints

#### 10. Get All Tests
**Endpoint:** `GET /portal/tests/`

**Description:** Get list of all available tests

**Headers:**
```
Authorization: Token <any_valid_token>
```

**Payload:** None (GET request)

**Access:** Both students and mentors

**Success Response (200):**
```json
[
    {
        "id": 1,
        "name": "Python Basics",
        "description": "Basic Python programming concepts including variables, loops, and functions",
        "created_at": "2024-08-01T09:00:00.000Z",
        "updated_at": "2024-08-01T09:00:00.000Z"
    },
    {
        "id": 2,
        "name": "Data Structures",
        "description": "Arrays, linked lists, stacks, queues, and basic algorithms",
        "created_at": "2024-08-02T10:00:00.000Z",
        "updated_at": "2024-08-02T10:00:00.000Z"
    }
]
```

---

#### 11. Create New Test
**Endpoint:** `POST /portal/tests/`

**Description:** Create a new test (mentor only)

**Headers:**
```
Authorization: Token <mentor_token>
Content-Type: application/json
```

**Payload:**
```json
{
    "name": "string (required)",
    "description": "string (required)"
}
```

**Example Request:**
```json
{
    "name": "Advanced Algorithms",
    "description": "Dynamic programming, graph algorithms, and complex problem solving"
}
```

**Access:** Mentors only

**Success Response (201):**
```json
{
    "message": "Test created successfully",
    "data": {
        "id": 3,
        "name": "Advanced Algorithms",
        "description": "Dynamic programming, graph algorithms, and complex problem solving",
        "created_at": "2024-08-03T12:00:00.000Z",
        "updated_at": "2024-08-03T12:00:00.000Z"
    }
}
```

---

#### 12. Get Specific Test
**Endpoint:** `GET /portal/tests/<int:test_id>/`

**Description:** Get details of a specific test

**Headers:**
```
Authorization: Token <any_valid_token>
```

**Payload:** None (GET request)

**Access:** Both students and mentors

**Success Response (200):**
```json
{
    "id": 1,
    "name": "Python Basics",
    "description": "Basic Python programming concepts including variables, loops, and functions",
    "created_at": "2024-08-01T09:00:00.000Z",
    "updated_at": "2024-08-01T09:00:00.000Z"
}
```

---

#### 13. Update Test
**Endpoint:** `PUT /portal/tests/<int:test_id>/`

**Description:** Update test details (mentor only)

**Headers:**
```
Authorization: Token <mentor_token>
Content-Type: application/json
```

**Payload:**
```json
{
    "name": "string (optional)",
    "description": "string (optional)"
}
```

**Example Request:**
```json
{
    "name": "Advanced Python Programming",
    "description": "Advanced Python concepts including decorators, generators, and async programming"
}
```

**Access:** Mentors only

**Success Response (200):**
```json
{
    "message": "Test updated successfully",
    "data": {
        "id": 1,
        "name": "Advanced Python Programming",
        "description": "Advanced Python concepts including decorators, generators, and async programming",
        "created_at": "2024-08-01T09:00:00.000Z",
        "updated_at": "2024-08-03T12:15:00.000Z"
    }
}
```

---

#### 14. Delete Test
**Endpoint:** `DELETE /portal/tests/<int:test_id>/`

**Description:** Delete a test (mentor only)

**Headers:**
```
Authorization: Token <mentor_token>
```

**Payload:** None (DELETE request)

**Access:** Mentors only

**Success Response (200):**
```json
{
    "message": "Test \"Advanced Python Programming\" deleted successfully"
}
```

---

### Test Score Management Endpoints

#### 15. Add Test Score
**Endpoint:** `POST /portal/test-scores/`

**Description:** Add a test score for a student (mentor only)

**Headers:**
```
Authorization: Token <mentor_token>
Content-Type: application/json
```

**Payload:**
```json
{
    "student_id": "integer (required)",
    "test_id": "integer (required)",
    "score": "integer (required, 0-100)"
}
```

**Example Request:**
```json
{
    "student_id": 1,
    "test_id": 1,
    "score": 85
}
```

**Access:** Mentors only

**Success Response (201):**
```json
{
    "message": "Test score added successfully",
    "data": {
        "id": 1,
        "test": {
            "id": 1,
            "name": "Python Basics",
            "description": "Basic Python programming concepts",
            "created_at": "2024-08-01T09:00:00.000Z",
            "updated_at": "2024-08-01T09:00:00.000Z"
        },
        "score": 85,
        "date_taken": "2024-08-03T12:30:00.000Z"
    }
}
```

---

#### 16. Update Test Score
**Endpoint:** `PUT /portal/test-scores/<int:score_id>/`

**Description:** Update an existing test score (mentor only)

**Headers:**
```
Authorization: Token <mentor_token>
Content-Type: application/json
```

**Payload:**
```json
{
    "score": "integer (required, 0-100)"
}
```

**Example Request:**
```json
{
    "score": 92
}
```

**Access:** Mentors only

**Success Response (200):**
```json
{
    "message": "Test score updated successfully",
    "data": {
        "id": 1,
        "test": {
            "id": 1,
            "name": "Python Basics",
            "description": "Basic Python programming concepts",
            "created_at": "2024-08-01T09:00:00.000Z",
            "updated_at": "2024-08-01T09:00:00.000Z"
        },
        "score": 92,
        "date_taken": "2024-08-03T12:30:00.000Z"
    }
}
```

---

#### 17. Delete Test Score
**Endpoint:** `DELETE /portal/test-scores/<int:score_id>/`

**Description:** Delete a test score (mentor only)

**Headers:**
```
Authorization: Token <mentor_token>
```

**Payload:** None (DELETE request)

**Access:** Mentors only

**Success Response (200):**
```json
{
    "message": "Test score deleted successfully"
}
```

---

## Error Responses

### Common Error Responses:

#### 400 Bad Request
```json
{
    "field_name": ["Error message"]
}
```

#### 401 Unauthorized
```json
{
    "detail": "Authentication credentials were not provided."
}
```

#### 403 Forbidden
```json
{
    "error": "You do not have permission to perform this action"
}
```

#### 404 Not Found
```json
{
    "detail": "Not found."
}
```

### Specific Error Examples:

#### Invalid Login
```json
{
    "non_field_errors": ["Invalid credentials"]
}
```

#### Duplicate Test Score
```json
{
    "non_field_errors": ["Test score already exists for this student and test"]
}
```

#### Invalid Score Range
```json
{
    "score": ["Score must be between 0 and 100"]
}
```

#### Student Accessing Mentor-Only Endpoint
```json
{
    "error": "Only mentors can create tests"
}
```

---

## Testing Guide

### Complete Testing Workflow

#### 1. Setup Data
First, create some test objects via Django admin:

```python
# Django shell or admin
Test.objects.create(
    name="Python Basics",
    description="Basic Python programming concepts"
)
Test.objects.create(
    name="Data Structures", 
    description="Arrays, linked lists, stacks, and queues"
)
```

#### 2. Student Registration and Profile Management
```bash
# Register student
curl -X POST http://localhost:8000/portal/register/student/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_student",
    "email": "alice@example.com",
    "password": "securepass123",
    "first_name": "Alice",
    "last_name": "Johnson",
    "leetcode": "alice_leetcode",
    "github": "alice_github",
    "bio": "CS student"
  }'

# Login as student
curl -X POST http://localhost:8000/portal/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice_student",
    "password": "securepass123"
  }'

# Get student profile
curl -X GET http://localhost:8000/portal/profile/student/ \
  -H "Authorization: Token <student_token>"

# Update student profile
curl -X PUT http://localhost:8000/portal/profile/student/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <student_token>" \
  -d '{
    "bio": "Updated bio content",
    "leetcode": "new_leetcode_handle"
  }'
```

#### 3. Mentor Registration and Operations
```bash
# Register mentor
curl -X POST http://localhost:8000/portal/register/mentor/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "dr_smith",
    "email": "smith@example.com",
    "password": "mentorpass123",
    "first_name": "John",
    "last_name": "Smith",
    "expertise": "Full Stack Development",
    "github": "drsmith_dev",
    "bio": "Senior software engineer"
  }'

# Login as mentor
curl -X POST http://localhost:8000/portal/login/ \
  -H "Content-Type: application/json" \
  -d '{
    "username": "dr_smith",
    "password": "mentorpass123"
  }'

# Get all students
curl -X GET http://localhost:8000/portal/students/ \
  -H "Authorization: Token <mentor_token>"

# Create new test
curl -X POST http://localhost:8000/portal/tests/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <mentor_token>" \
  -d '{
    "name": "Advanced Algorithms",
    "description": "Dynamic programming and graph algorithms"
  }'

# Add test score
curl -X POST http://localhost:8000/portal/test-scores/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <mentor_token>" \
  -d '{
    "student_id": 1,
    "test_id": 1,
    "score": 85
  }'
```

#### 4. Permission Testing
```bash
# Student trying to add test score (should fail)
curl -X POST http://localhost:8000/portal/test-scores/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Token <student_token>" \
  -d '{
    "student_id": 1,
    "test_id": 1,
    "score": 85
  }'

# Expected response: 403 Forbidden
```

---

## Complete URL Summary

| Method | URL | Access | Description |
|--------|-----|--------|-------------|
| POST | `/portal/register/student/` | Public | Register new student |
| POST | `/portal/register/mentor/` | Public | Register new mentor |
| POST | `/portal/login/` | Public | Login (both roles) |
| GET | `/portal/profile/student/` | Student | Get own profile |
| PUT | `/portal/profile/student/` | Student | Update own profile |
| GET | `/portal/profile/student/<id>/` | Student/Mentor | Get specific student profile |
| PUT | `/portal/profile/student/<id>/` | Student | Update own profile |
| GET | `/portal/profile/mentor/` | Mentor | Get mentor profile |
| PUT | `/portal/profile/mentor/` | Mentor | Update mentor profile |
| GET | `/portal/students/` | Mentor | Get all students |
| GET | `/portal/tests/` | Both | Get all tests |
| POST | `/portal/tests/` | Mentor | Create new test |
| GET | `/portal/tests/<id>/` | Both | Get specific test |
| PUT | `/portal/tests/<id>/` | Mentor | Update test |
| DELETE | `/portal/tests/<id>/` | Mentor | Delete test |
| POST | `/portal/test-scores/` | Mentor | Add test score |
| PUT | `/portal/test-scores/<id>/` | Mentor | Update test score |
| DELETE | `/portal/test-scores/<id>/` | Mentor | Delete test score |

---

## Notes

- All endpoints require authentication except registration and login
- Students can only update their own profiles
- Mentors have full access to test and test score management
- All PUT requests support partial updates
- Tokens are automatically generated upon registration and login
- Test names must be unique (case-insensitive)
- Test scores must be between 0-100
- No duplicate test scores allowed for same student-test combination