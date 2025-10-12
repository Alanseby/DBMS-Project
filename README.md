# Freelance Project Management System (FPRMS)

A comprehensive web-based platform for managing freelance projects, connecting clients with freelancers, and tracking project milestones.

## 🌟 Features

- **User Management**: Support for Clients, Freelancers, and Admins
- **Project Management**: Create, edit, and manage projects
- **Bidding System**: Freelancers can bid on open projects
- **Milestone Tracking**: Break projects into milestones with sequential completion
- **Review System**: Rate and review completed work
- **User Profiles**: Detailed freelancer profiles with skills and portfolio

## 🚀 Quick Start with Online Database

**Want to share this with friends? Follow these steps:**

1. **Set up online database** (5 minutes):
   ```bash
   # See QUICK_START.md for detailed instructions
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**:
   ```bash
   copy .env.example .env
   # Edit .env with your database URL
   ```

4. **Initialize database**:
   ```bash
   python migrate_to_online.py
   ```

5. **Run the application**:
   ```bash
   python app.py
   ```

6. **Access the app**: http://localhost:5000

## 📚 Documentation

- **[Quick Start Guide](QUICK_START.md)** - Get up and running in 5 minutes
- **[Online Database Setup](ONLINE_DATABASE_SETUP.md)** - Detailed guide for all database options
- **[Migration Script](migrate_to_online.py)** - Tool to set up your online database

## 🗄️ Database Support

This application supports both **MySQL** and **PostgreSQL** databases:

- **Local Development**: MySQL (default)
- **Online/Production**: PostgreSQL (Supabase, Railway, Render) or MySQL (PlanetScale)

Simply set your `DATABASE_URL` in the `.env` file!

## 👥 User Roles

### Client
- Create and manage projects
- Review freelancer bids
- Accept bids and assign projects
- Create and manage milestones
- Review completed work

### Freelancer
- Browse open projects
- Submit bids with cover letters
- Work on assigned projects
- Submit milestone deliverables
- Build portfolio and receive reviews

### Admin
- Manage all users
- Oversee all projects
- System-wide analytics

## 🛠️ Technology Stack

- **Backend**: Flask (Python)
- **Database**: SQLAlchemy (MySQL/PostgreSQL)
- **Authentication**: Flask-Login
- **Frontend**: HTML, CSS, JavaScript
- **Deployment**: Gunicorn-ready

## 📦 Project Structure

```
DBMS-Project/
├── app.py                      # Main application file
├── models.py                   # Database models
├── config.py                   # Configuration
├── requirements.txt            # Python dependencies
├── migrate_to_online.py        # Database migration tool
├── templates/                  # HTML templates
│   ├── dashboard/             # Role-specific dashboards
│   ├── projects/              # Project management
│   ├── profile/               # User profiles
│   └── ...
└── static/                     # CSS, JS, images
```

## 🔒 Security

- Passwords are hashed using Werkzeug security
- Environment variables for sensitive data
- `.gitignore` configured to protect credentials
- Session-based authentication

## 🌐 Deployment Options

### Option 1: Shared Database (Local Apps)
Friends run the app locally but connect to the same online database.

### Option 2: Full Deployment (Recommended)
Deploy to platforms like:
- **Render** (Free tier available)
- **Railway** (Free tier available)
- **Heroku** (Paid)

See `ONLINE_DATABASE_SETUP.md` for deployment guides.

## 🤝 Sharing with Friends

1. **Share Database Access**:
   - Give friends your `.env` file (securely!)
   - They run the app locally
   - Everyone uses the same database

2. **Deploy Online**:
   - Deploy to Render/Railway
   - Share the URL
   - No setup needed for friends!

## 📝 Sample Credentials

After running `migrate_to_online.py` with sample data:

- **Admin**: admin@fprms.com / admin123
- **Client**: client@fprms.com / client123
- **Freelancer**: freelancer@fprms.com / freelancer123

## 🐛 Troubleshooting

See `QUICK_START.md` for common issues and solutions.

## 📄 License

This project is for educational purposes (DBMS Micro Project).

## 👨‍💻 Contributing

This is a micro project for DBMS course. Feel free to fork and enhance!

---

**Need help?** Check out the guides:
- 📖 [Quick Start Guide](QUICK_START.md)
- 🌐 [Online Database Setup](ONLINE_DATABASE_SETUP.md)

**Ready to go online?** Run: `python migrate_to_online.py`
