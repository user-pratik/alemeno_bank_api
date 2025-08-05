# 💳 Alemeno Credit Approval System

A containerized, production-ready Django REST API for handling customer registration, loan approvals, and EMI calculations.

---

## ⚙️ Tech Stack
- **Framework:** Django 4+, Django REST Framework
- **Database:** PostgreSQL
- **Containerization:** Docker & Docker Compose
- **Extras:** Background Excel data ingestion

---

## 📁 Directory Structure

```bash
alemeno_credit_backend/
├── core/                  # Django app: models, views, serializers, tests
├── customer_data.xlsx     # Sample customer data
├── loan_data.xlsx         # Sample loan data
├── manage.py              # Django CLI entrypoint
├── requirements.txt       # Python dependencies
├── Dockerfile             # Image configuration
├── docker-compose.yml     # Multi-service orchestration
├── .env.example           # Environment variable template
└── README.md              # Project documentation
🚀 Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/sseth345/alemeno_credit_backend.git
cd alemeno_credit_backend
2. Setup Environment Variables
Rename .env.example to .env:

bash
Copy
Edit
cp .env.example .env
Edit values as needed:

env
Copy
Edit
DB_NAME=credit_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
3. Build & Run with Docker
bash
Copy
Edit
docker compose up --build -d
4. Apply Migrations
bash
Copy
Edit
docker compose exec web python manage.py migrate
5. (Optional) Load Initial Excel Data
bash
Copy
Edit
docker compose exec web python manage.py ingest_initial_data customer_data.xlsx loan_data.xlsx
🔌 API Endpoints
Method	Endpoint	Description
POST	/api/register/	Register a new customer
POST	/api/check-eligibility/	Check loan eligibility
POST	/api/create-loan/	Create a loan (if eligible)
GET	/api/view-loan/<loan_id>/	Retrieve specific loan info
GET	/api/view-loans/<cust_id>/	View all loans for a customer

📦 Example Request
http
Copy
Edit
POST /api/register/
Content-Type: application/json
json
Copy
Edit
{
  "first_name": "Sita",
  "last_name": "Verma",
  "age": 29,
  "phone_number": "9876543210",
  "monthly_income": 55000
}
🧪 Running Tests
bash
Copy
Edit
docker compose exec web python manage.py test core
🛑 Stop Services
bash
Copy
Edit
docker compose down        # Stop containers
docker compose down -v     # Stop + remove volumes
🧩 Troubleshooting
command not found: Ensure Docker & Docker Compose are installed

API not working? → Run: docker compose logs -f web

Port issues? → Make sure ports 8000 and 5432 aren’t in use

🔐 Notes
Never commit .env to version control

Keep API docs up to date with code

Entire project runs in Docker—no manual setup required

📬 For questions, open an issue or contact the maintainer.

markdown
Copy
Edit

Let me know if you want:
- Swagger/OpenAPI integration
- GitHub Actions for CI
- Auto `.env` setup script

I'll plug it in.
