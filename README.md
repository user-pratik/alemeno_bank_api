# Alemeno Credit Approval System

A **production-ready**, containerized **Django REST API** that manages customer registration, loan approvals, and EMI calculations for Alemeno's Credit Approval System assignment.

---

## 🛠️ Tech Stack

- **Backend**: Django 4+, Django REST Framework  
- **Database**: PostgreSQL  
- **Containerization**: Docker, Docker Compose  
- **Data Handling**: Background ingestion of Excel files

---

## 📁 Project Structure

```text
alemeno_credit_backend/
├── core/                    # Django app: models, views, serializers, tests
├── customer_data.xlsx       # Sample customer data
├── loan_data.xlsx           # Sample loan data
├── manage.py                # Django CLI entrypoint
├── requirements.txt         # Python dependencies
├── Dockerfile               # Image configuration
├── docker-compose.yml       # Multi-service orchestration
├── .env.example             # Environment variable template
└── README.md                # Project documentation
```

---

## 🚀 Getting Started

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/sseth345/alemeno_credit_backend.git
cd alemeno_credit_backend
```

### 2️⃣ Setup Environment Variables

Create a `.env` file using the example template:

```bash
cp .env.example .env
```

Edit values as needed:

```env
DB_NAME=cas_db
DB_USER=postgres
DB_PASSWORD=password
DB_HOST=db
DB_PORT=5432
```

### 3️⃣ Build & Run with Docker

```bash
docker compose up --build -d
```

### 4️⃣ Apply Migrations

```bash
docker compose exec web python manage.py migrate
```

### 5️⃣ (Optional) Load Initial Data

```bash
docker compose exec web python manage.py ingest_initial_data customer_data.xlsx loan_data.xlsx
```

---

## 📡 API Endpoints

| Endpoint                      | Method | Description                   |
|------------------------------|--------|-------------------------------|
| `/api/register/`             | POST   | Register a new customer       |
| `/api/check-eligibility/`    | POST   | Check loan eligibility        |
| `/api/create-loan/`          | POST   | Create a new loan             |
| `/api/view-loan/<loan_id>/`  | GET    | View a specific loan          |
| `/api/view-loans/<cust_id>/` | GET    | List all loans for a customer |

---

### 🔸 Sample: Register Customer

```http
POST /api/register/
Content-Type: application/json

{
  "first_name": "Sita",
  "last_name": "Verma",
  "age": 29,
  "phone_number": "9876543210",
  "monthly_income": 55000
}
```

---

## ✅ Run Tests

```bash
docker compose exec web python manage.py test core
```

---

## 🛑 Stopping the Project

```bash
docker compose down         # Stop services
# OR
docker compose down -v      # Stop and remove volumes
```

---
📬 Contact
For questions, feedback, or collaboration opportunities, feel free to reach out:

Pratik Anand

📧 Email: pratik.csdev@gmail.com

🧑‍💻 GitHub: github.com/user-pratik

