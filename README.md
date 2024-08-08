# FastAPI User Authentication Template

This project is a FastAPI-based user authentication system that provides basic user registration and login functionality. It can be easily set up and run by following the steps below.

## Features

- User registration
- User authentication (login)
- JWT-based token generation

## Prerequisites

- Docker installed
- Docker Compose installed

## Getting Started

### Setting Up Environment Variables

1. Create a `.env` file in the root directory of the project by copying the provided `env.template` file:

```bash
cp env.template .env
```

2. Open the `.env` file and fill in the necessary values, such as database credentials and JWT secret key.

- How to create a secret key(https://fastapi.tiangolo.com//tutorial/security/oauth2-jwt/#handle-jwt-tokens)

### Building and Running the Application

1. Build the Docker images:

```bash
docker compose build
```

2. Start the containers:

```bash
docker compose up
```

The API will be available at `http://localhost:8080`. You can access the API documentation at `http://localhost:8080/docs`.

## API Endpoints

- `/api/register` - Register a new user
- `/api/login` - User login and token generation

For detailed API documentation, please refer to the Swagger UI at `/docs` endpoint when the server is running.

## API Usage

### User Registration

To register a new user, send a POST request to `/api/register` with the following JSON body:

```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

### User Login

To log in and receive an access token, send a POST request to `/api/login` with form-data containing:

- `username`: The user's email address
- `password`: The user's password

The response will include an access token that can be used for authenticated requests.

## Customization

This template provides a basic structure for user authentication. You can extend it by adding more features such as user profile management, password reset functionality, or additional security measures.
