# BloomWealth - Mututal Fund Brokerage Firm

### Overview of the components of the project:

1. **Core Files**:
   - `bloom.py`: The main entry point of the application.
   - `config.py`: Configuration settings, including database and environment variables.
   - `requirements.txt`: Python dependencies.

2. **Application Components**:
   - `bloom/`: Contains forms, models, routes, templates, and utilities.
   - `bloom/models/`: Database models.
   - `bloom/routes/`: API and web routes.
   - `bloom/templates/`: HTML templates.
   - `bloom/utils/rapid_api.py`: Integration with RapidAPI.

3. **Environment & Database**:
   - `.env`: Environment variables file.
   - `instance/mutual_fund.db`: SQLite database.

4. **Migrations**:
   - `migrations/`: Database migration scripts.

### Documentation: Setting Up and Running the Application

#### Prerequisites
Before setting up the application, ensure you have the following installed:
- Python 3.9 or higher
- Pip (Python package manager)
- SQLite3 (for database usage)
- Virtual environment tool (optional but recommended)

---

### Step 1: Clone or Extract the Project
Ensure the project files are extracted to your local machine.

```bash
git clone "https://github.com/RanjithPoojary/BloomWealth"
```
---

### Step 2: Set Up a Virtual Environment (Optional)
To isolate dependencies, create and activate a virtual environment:
```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

---

### Step 3: Install Dependencies
Install the required Python packages:
```bash
pip install -r requirements.txt
```

---

### Step 4: Configure Environment Variables
1. Rename the `.env` file in the project directory to remove the leading dot if your system hides it. (`.env` → `env` on Windows if needed).
2. Open `.env` and update the following keys:
   - `DATABASE_URL`: Set the path to your SQLite database, e.g., `sqlite:///instance/mutual_fund.db`.
   - `RAPID_API_KEY`: Add your RapidAPI key here for API integration.

Example `.env` content:
```ini
DATABASE_URL=sqlite:///instance/mutual_fund.db
RAPID_API_KEY=your-rapidapi-key-here
```

---

### Step 5: Run Initial Database Migrations
Apply the database migrations to set up the required tables:
```bash
flask db upgrade
```

This will use Alembic to create the necessary tables as defined in the migration scripts.

---

### Step 6: Run the Application
Start the application:
```bash
flask run
```

The application will be accessible at `http://127.0.0.1:5000`.

---

### Optional: Create Initial Database Migration Scripts
If additional database tables or modifications are needed, use the following commands:

1. **Create a New Migration**:
   ```bash
   flask db migrate -m "Description of migration"
   ```

2. **Apply the Migration**:
   ```bash
   flask db upgrade
   ```

---

### Step 7: Verify RapidAPI Integration
Test the functionality that relies on RapidAPI by invoking related features. If errors occur, confirm the `RAPID_API_KEY` is correctly set in `.env` and matches your RapidAPI subscription.

---
