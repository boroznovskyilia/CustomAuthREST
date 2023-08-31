# CustomAuthREST 
Welcome to the Custom Authorization and Authentication System built with FastAPI! This project provides a powerful authentication and authorization system with CRUD operations, JWT tokens, OAuth2, and more.

## Features
User Registration and Authentication:** Secure user registration and login system with password hashing.
- **Custom Authorization Roles:** Implement different authorization roles such as Super User with enhanced privileges.
- **CRUD Operations:** Create, Read, Update, and Delete user records with comprehensive API endpoints.
- **Search Users by Name:** Effortlessly search for users by their names.
- **Get All Users:** Retrieve a list of all registered users.
- **JWT Token-based Authentication:** Securely authenticate users with JSON Web Tokens (JWT).
- **OAuth2 Support:** Integrate OAuth2 for third-party authentication.
- **PostgreSQL Database:** Store user data in a robust PostgreSQL database.
- **SQLAlchemy ORM:** Utilize the powerful SQLAlchemy ORM for efficient database interactions.
- **Alembic for Database Migrations:** Seamlessly manage database schema changes with Alembic migrations.
- **Redis for JWT Token Blacklisting:** Enhance security by blacklisting JWT tokens with Redis.
- **Pydantic Models for Data Validation:** Validate and sanitize user data with Pydantic models.
- **Asynchronous FastAPI Application:** Leverage FastAPI's asynchronous capabilities for efficient I/O handling.
- **Docker and Docker Compose Integration:** Easily deploy the application using Docker and Docker Compose.

## Screenshots
![Снимок экрана 2023-08-31 195546](https://github.com/boroznovskyilia/CustomAuthREST/assets/91383856/7dbb3d5a-7fec-4393-8d9b-182d7061e2d3)
![Снимок экрана 2023-08-31 195557](https://github.com/boroznovskyilia/CustomAuthREST/assets/91383856/bdeab73c-9648-4048-833d-312a5be93ffd)

## Installation and Usage

1. Clone this repository:
   ```bash
   git clone https://github.com/boroznovskyilia/CustomAuthREST.git
   
  Run app with docker:
    docker-compose up -d
     
     
