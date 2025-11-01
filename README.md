# Order Management System API

A complete FastAPI-based order management system with user authentication, JWT tokens, and role-based access control.

Features:

User Authentication: JWT-based authentication with secure password hashing

User Registration: Register as regular user or superuser

Role-Based Access Control: Different endpoints for regular users and superusers

Order Management: Create, read, update, and delete orders

User-Specific Orders: Users can only access their own orders

Superuser Features: Superusers can view all orders and update order status

Interactive API Documentation: Built-in Swagger UI and ReDoc

Tech Stack

FastAPI: Modern Python web framework

SQLAlchemy: SQL toolkit and ORM

PostgreSQL/SQLite: Database

Pydantic: Data validation

python-jose: JWT token generation

passlib: Password hashing with bcrypt

OrderSystem/
├── app/
│   ├── main.py               # FastAPI application entry point
│   ├── models.py             # SQLAlchemy database models
│   ├── schemas.py            # Pydantic request/response schemas
│   ├── database.py           # Database configuration
│   ├── auth.py               # Authentication utilities
│   └── routers/
│       ├── auth.py           # Authentication endpoints
│       └── orders.py         # Order management endpoints
└── README.md                
