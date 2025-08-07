## Cap Table Backend

This backend project implements the core functionalities of a Cap Table (Capitalization Table) management system. 
It is built using FastAPI with PostgreSQL as the database, containerized using Docker, and designed to be run locally.

The system provides endpoints to manage companies, stakeholders, 
share classes, and share allocations. The project architecture separates concerns cleanly across modules 
(e.g., models, routes, services), following clean code and scalable project structure practices.

### Technical Approach & Architectural Decisions

--- Framework: FastAPI was chosen for its speed, simplicity, and built-in documentation via Swagger.

--- Database: PostgreSQL provides strong support for relational data, ideal for modeling cap tables.

--- ORM: SQLAlchemy is used for database interactions, with Alembic for migrations.

--- Docker: The project is fully containerized with Docker, ensuring consistent local development environments.

--- Modular Structure: The project is organized into folders such as models, schemas, routes, and services to promote maintainability and scalability.

--- Auditing: SQLAlchemy event listeners are used to log CRUD operations in the audit_log table for transparency and debugging.

 ### Prerequisites

Ensure the following are installed:

-- Docker

-- Docker Compose

-- Git

Local Setup Instructions

 Step 1: Clone the Repository

git clone https://github.com/ngounou-tp/cap-table-backend.git

Step 2: Add Environment Variables
Create a .env file based on the provided .env.example.

POSTGRES_DB=cap_table
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DATABASE_URL=postgresql://postgres:postgres@db:5432/cap_table

Step 3: Run the Application with Docker

docker-compose up --build

step 4:  Setup Virtual Environment & Dependencies

 -- If you haven’t already :
 # Create a virtual environment
python -m venv .venv

 -- Install dependencies listed in requirements.txt
 pip install -r requirements.txt

---  Apply Migration

 alembic upgrade head
 
-- Start the Development Server

 uvicorn app.main:app --reload


# Activate it
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate





FastAPI server at http://localhost:8000

PostgreSQL DB at localhost:5432

-- Step 4: Access API Docs
Visit http://localhost:8000/docs to test the endpoints using Swagger UI.

-- Primary AI Tools Used

ChatGPT (GPT-4o) – Used extensively to:

Set up FastAPI project structure

Write and refactor SQLAlchemy models

Generate boilerplate code for routes and services

Configure Alembic for database migrations

GitHub Copilot – Used to speed up repetitive coding patterns

💬 Key Prompts Used
Here are some examples of prompts used to guide the AI tools during development:

"Generate a SQLAlchemy model for a Cap Table with relationships between Company, ShareClass, and Stakeholder."

"Write a FastAPI route to allocate shares to a stakeholder under a specific share class."

"Help set up Alembic migrations for FastAPI and PostgreSQL in Docker."

"Track updates on SQLAlchemy models using event listeners and log them to an audit table."

"Explain how to organize FastAPI routes, schemas, services, and models in a modular project."




Admin User
Email (username): admin@example.com

Password: admin123

Role: admin

✅ Shareholder User
Email (username): shareholder@example.com

Password: share123

Role: shareholder