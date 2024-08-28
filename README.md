# To-Do List API

This project is a To-Do List API built using FastAPI, MySQL, and JWT-based authentication. The API allows users to register, log in, and manage their to-do items securely.

## Features

- **User Authentication**: Secure user registration and login using JWT tokens.
- **To-Do Management**: CRUD operations for to-do items.
- **MySQL Database**: Persistent storage of user information and to-do items.
- **Password Hashing**: Secure storage of user passwords using hashing.
- **API Documentation**: Auto-generated API documentation with Swagger UI.

## Technologies Used

- **FastAPI**: A modern, fast (high-performance), web framework for building APIs with Python 3.7+.
- **SQLAlchemy**: SQL toolkit and Object-Relational Mapping (ORM) library for Python.
- **Pydantic**: Data validation and settings management using Python type annotations.
- **JWT (JSON Web Tokens)**: Secure token-based authentication.
- **MySQL**: Relational database management system.
- **Alembic**: Database migrations tool for SQLAlchemy.

## Getting Started

### Prerequisites

- **Python 3.7+**: Make sure Python is installed on your system. [Download Python](https://www.python.org/downloads/)
- **MySQL**: Install MySQL and create a database for this project.

### Installation

1. **Clone the Repository**:

    ```bash
    git clone https://github.com/yourusername/todo_app.git
    cd todo_app
    ```

2. **Create a Virtual Environment**:

    ```bash
    python -m venv venv
    ```

3. **Activate the Virtual Environment**:

    - On Windows:
      ```bash
      venv\Scripts\activate
      ```
    - On macOS and Linux:
      ```bash
      source venv/bin/activate
      ```

4. **Install Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

5. **Set Up Environment Variables**:

    Create a `.env` file in the project root and add the following environment variables. Replace the placeholders with your actual MySQL credentials and secret key:

    ```env
    DATABASE_URL=mysql+mysqlconnector://username:password@localhost/todo_db
    SECRET_KEY=your_secret_key
    ```

6. **Set Up Database**:

    - Initialize Alembic for database migrations:
    
      ```bash
      alembic init alembic
      ```

    - Edit `alembic.ini` and `alembic/env.py` to configure your database connection and target metadata.

    - Create and apply the initial database migration:
    
      ```bash
      alembic revision --autogenerate -m "Initial migration"
      alembic upgrade head
      ```

### Running the Application

Start the FastAPI server with Uvicorn:

```bash
uvicorn main:app --reload
