Alemeno Credit Approval Backend

A containerized Django REST API for managing customer registrations, verifying loan eligibility, creating loans, and tracking loan records. The system also supports background ingestion of customer and loan data from Excel files and calculates EMI using compound interest.

🛠️ Requirements

Docker

Docker Compose

Git

⚙️ Setup

Clone the Repository

git clone https://github.com/sseth345/alemeno_credit_backend.git
cd alemeno_credit_backend

Configure Environment Variables

Copy the sample config and update values as needed:

cp .env.example .env

🚀 Run with Docker

Start the backend and PostgreSQL database containers:

docker compose up --build -d

Run database migrations:

docker compose exec web python manage.py migrate

(Optional) Load initial data from Excel files:

docker compose exec web python manage.py ingest_initial_data customer_data.xlsx loan_data.xlsx

🔌 API Endpoints

Endpoint

Method

Description

/api/register/

POST

Register a new customer

/api/check-eligibility/

POST

Check loan eligibility

/api/create-loan/

POST

Create a loan

/api/view-loan/<loan_id>/

GET

View a specific loan

/api/view-loans/<customer_id>/

GET

View all loans for a customer

✅ Testing

Run unit tests:

docker compose exec web python manage.py test core

🛑 Stop Services

docker compose down
# Add `-v` to remove volumes as well

📁 Project Layout

alemeno_credit_backend/
├── core/              # App logic
├── Dockerfile
├── docker-compose.yml
├── .env.example
├── customer_data.xlsx
├── loan_data.xlsx

🔐 Notes

Never commit .env to version control.

Keep dependencies in requirements.txt updated.

Use docker compose logs web for debugging.
