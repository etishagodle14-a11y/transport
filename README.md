# TransportFlow ERP 🚚

A digital ERP system built to modernize transport businesses — replacing paper-based records with a centralized, real-time management platform.

---

## The Problem It Solves

Small and medium transport businesses in India rely on manual registers and paper receipts ("Biltys") to track shipments, revenue, and payments. This leads to calculation errors, lost records, and no visibility into real-time profit/loss.

**TransportFlow ERP eliminates all of that.**

---

## Features

- **Live Financial Dashboard** — Automatically calculates Revenue, Expenses, and Net Profit in real time. No manual math.
- **Pending Payments Tracker** — Instantly shows which clients owe payments and by how much.
- **Bilty Generation** — Prints a professional shipment receipt the moment a new trip is added.
- **Shipment Management** — Add, update, and manage transport records from a single interface.
- **Secure Authentication** — Login system to protect business data.

---

## Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python, Django |
| Frontend | Bootstrap 5, Django Templates |
| Database | SQLite |
| Auth | Django built-in authentication |

---

## Screenshots

> _Add screenshots here — dashboard view, Bilty print view, and shipment list page._
> _Tip: Use `![Dashboard](screenshots/dashboard.png)` after adding images to a `/screenshots` folder._

---

## Getting Started

Follow these steps to run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/etishagod/transport.git
cd transport

# 2. Create a virtual environment
python -m venv venv
source venv/bin/activate        # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply database migrations
python manage.py migrate

# 5. Create a superuser (admin login)
python manage.py createsuperuser

# 6. Run the development server
python manage.py runserver
```

Then open your browser at `http://127.0.0.1:8000`

---

## Project Structure

```
transport/
├── manage.py
├── requirements.txt
├── transportflow/          # Main Django app
│   ├── models.py           # Shipment, Revenue, Expense models
│   ├── views.py            # Dashboard, Bilty, CRUD logic
│   ├── urls.py
│   └── templates/          # HTML templates (Bootstrap)
└── db.sqlite3
```

---

## What I Learned

- Designing relational database models for real-world business logic
- Writing backend calculations that replace manual processes entirely
- Generating printable document outputs (Biltys) from Django views
- Building role-based access using Django's authentication system

---

## Future Improvements

- [ ] Migrate from SQLite to PostgreSQL for production use
- [ ] Add REST API endpoints using Django REST Framework
- [ ] Deploy live on Railway or Render
- [ ] Add monthly/yearly profit analytics with charts (Matplotlib / Chart.js)
- [ ] Multi-user support with role-based permissions (Owner, Driver, Accountant)

---

## Author

**Etisha Godle**
- GitHub: [@etishagod](https://github.com/etishagod)
- LinkedIn: [Etisha Godle](https://www.linkedin.com/in/etisha-godle-636744275)
- Email: etishagodle14@gmail.com

---

> Built with Django & Python | Open to collaborations and feedback
