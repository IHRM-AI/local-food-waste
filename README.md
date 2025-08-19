# Local Food Wastage Management System

## Overview

The **Local Food Wastage Management System** is a Streamlit-based web application designed to connect food providers (such as restaurants, shops, and individuals) with receivers (such as NGOs, shelters, and food banks). The system aims to minimize food wastage by facilitating the donation and claiming of surplus food items, and providing actionable insights through data analytics.

---

## Features

- **Provider and Receiver Management:** Register, list, and manage food providers and receivers with detailed contact and location information.
- **Food Listings:** Providers can list surplus food items with quantity, expiry date, type, and meal category.
- **Claims Workflow:** Receivers can browse available food items and claim them. Claim status and timestamps are tracked.
- **Dashboard & Insights:** Real-time stats and charts including:
  - Total quantity available
  - Top cities by listings
  - Most claimed meal types
  - Breakdown by provider/receiver type, food types, and claim statuses
- **Filtering:** Filter listings and insights by city, food type, provider type, and meal type.
- **Database Seeding:** Sample data for providers, receivers, and food listings for demonstration and testing.

---

## Tech Stack

- **Backend:** Python, SQLite, SQLAlchemy (ORM)
- **Frontend:** Streamlit
- **Data Management:** CSV seeding, relational database
- **Version Control:** Git & GitHub

---

## Project Structure

```plaintext
local-food-waste/
│
├── app.py                # Main Streamlit app entry point
├── src/
│   ├── models.py         # SQLAlchemy models for database schema
│   ├── seed_data.py      # Script to seed the SQLite database with sample data
│   └── queries.py        # Database queries and utility functions
│
├── pages/
│   ├── Dashboard.py      # Dashboard and insights page
│   ├── Claims.py         # Claims management page
│   ├── Listings.py       # Food listings page
│   └── Providers.py      # Provider management page
│
├── data/
│   ├── providers.csv     # Sample provider data (name, type, address, city, contact)
│   ├── receivers.csv     # Sample receiver data
│   └── food_listings.csv # Sample food listings data
│
├── local.db              # SQLite database file (auto-generated)
├── requirements.txt      # Python dependencies
└── README.md             # Project documentation
```

---

## Setup Instructions

### 1. **Clone the Repository**

```bash
git clone https://github.com/IHRM-AI/local-food-waste.git
cd local-food-waste
```

### 2. **Set Up Virtual Environment**

```bash
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate
```

### 3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

### 4. **Seed the Database**

**If starting fresh, remove any existing database:**

```bash
rm local.db
```

**Run the seed script:**

```bash
python -X dev -m src.seed_data
```

### 5. **Run the Streamlit App**

```bash
streamlit run app.py
```

The app will launch at [http://localhost:8501](http://localhost:8501).

---

## Usage Guide

- **Dashboard:** View key food wastage insights, stats, and analytics.
- **Providers:** Add, edit, or view provider details.
- **Listings:** Providers can add food items, view current listings.
- **Claims:** Receivers can claim food, view claim status/history.
- **Filters:** Use sidebar filters to narrow down listings and insights.

---

## Database Schema

- **Provider**
  - `Provider_ID`: Primary Key
  - `Name`
  - `Type`
  - `Address`
  - `City`
  - `Contact`
- **Receiver**
  - `Receiver_ID`: Primary Key
  - `Name`
  - `Type`
  - `City`
- **FoodListing**
  - `Food_ID`: Primary Key
  - `Food_Name`
  - `Quantity`
  - `Expiry_Date`
  - `Provider_ID`: Foreign Key
  - `Provider_Type`
  - `Location`
  - `Food_Type`
  - `Meal_Type`
- **Claim**
  - `Claim_ID`: Primary Key
  - `Food_ID`: Foreign Key
  - `Receiver_ID`: Foreign Key
  - `Status`
  - `Timestamp`

---

## Troubleshooting

- **Port Already in Use:** If `localhost:8501` is busy, kill the process or use a different port:
  ```bash
  streamlit run app.py --server.port 8502
  ```
- **Database Errors:** If you see "no such column" or schema errors, reseed your database:
  ```bash
  rm local.db
  python -X dev -m src.seed_data
  ```
- **Streamlit Errors:** For input forms, use `st.date_input` and `st.time_input` for date/time fields.

---

## Contribution Guide

1. Fork the repository and create your feature branch (`git checkout -b feature/fooBar`)
2. Commit your changes (`git commit -am 'Add some fooBar'`)
3. Push to the branch (`git push origin feature/fooBar`)
4. Create a new Pull Request

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Contact

For any issues or questions, open an issue on [GitHub Issues](https://github.com/IHRM-AI/local-food-waste/issues) or contact the maintainer at [github.com/IHRM-AI](https://github.com/IHRM-AI).
