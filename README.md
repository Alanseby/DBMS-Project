# Freelance Project Management System

A comprehensive web application for managing freelance projects, bids, and milestones.

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- MySQL or PostgreSQL database (MySQL recommended for Windows)
- pip (Python package manager)

### 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd DBMS-Project
   ```

2. **Set up a virtual environment**
   ```bash
   # Windows
   python -m venv venv
   .\venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   Create a `.env` file in the root directory with:
   ```env
   FLASK_APP=app.py
   FLASK_ENV=development
   SECRET_KEY=your-secret-key-here
   
   # For MySQL (recommended for Windows)
   DATABASE_URL=mysql+pymysql://username:password@localhost/freelance_db
   
   # OR for PostgreSQL
   # DATABASE_URL=postgresql+pg8000://username:password@localhost:5432/freelance_db
   ```

5. **Initialize the database**
   ```bash
   flask shell
   >>> from app import db
   >>> db.create_all()
   >>> exit()
   ```

6. **Run the application**
   ```bash
   flask run
   ```
   Open your browser and visit: `http://localhost:5000`

## 📂 Project Structure

```
DBMS-Project/
├── app.py                # Main application
├── config.py            # Configuration settings
├── models.py            # Database models
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables
├── static/              # Static files (CSS, JS, images)
└── templates/           # HTML templates
    ├── admin/           # Admin interface
    ├── bids/            # Bid management
    ├── profile/         # User profiles
    └── projects/        # Project management
```

## 🔧 Troubleshooting

### Database Connection Issues
- Ensure your database server is running
- Verify database credentials in `.env`
- For PostgreSQL, you might need to add `?sslmode=disable` to the connection string

### Common Errors
- **Module not found**: Activate virtual environment and run `pip install -r requirements.txt`
- **Database errors**: Make sure the database exists and the user has proper permissions

## 📝 First Time Setup

1. After starting the application, register a new account
2. The first account will have admin privileges
3. You can then create projects, place bids, and manage milestones

## 📄 License

This project is licensed under the MIT License.
