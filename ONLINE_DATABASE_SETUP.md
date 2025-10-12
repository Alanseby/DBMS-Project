# Online Database Setup Guide

This guide will help you migrate your DBMS project to an online database so your friends can access it.

## Recommended Options

### Option 1: Supabase (PostgreSQL) - **RECOMMENDED**
**Best for:** Easy setup, generous free tier, great for beginners

#### Steps:
1. Go to [supabase.com](https://supabase.com)
2. Sign up with GitHub/Google
3. Click "New Project"
4. Fill in:
   - Project name: `fprms-db` (or any name)
   - Database password: Create a strong password
   - Region: Choose closest to you
5. Wait 2-3 minutes for setup
6. Go to **Settings** → **Database**
7. Scroll to **Connection String** → **URI**
8. Copy the connection string (looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres`)
9. Replace `[YOUR-PASSWORD]` with your actual password
10. Update your `.env` file with this URL

**Free Tier:**
- 500MB database
- Unlimited API requests
- 50,000 monthly active users

---

### Option 2: Railway (PostgreSQL/MySQL)
**Best for:** Simple deployment, supports both PostgreSQL and MySQL

#### Steps:
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Click "New Project" → "Provision PostgreSQL" (or MySQL)
4. Click on the database service
5. Go to **Variables** tab
6. Copy the `DATABASE_URL` value
7. Update your `.env` file with this URL

**Free Tier:**
- $5 credit/month
- 500 hours execution time

---

### Option 3: PlanetScale (MySQL)
**Best for:** MySQL users, serverless database

#### Steps:
1. Go to [planetscale.com](https://planetscale.com)
2. Sign up with GitHub
3. Create new database
4. Click "Connect"
5. Select "General" connection
6. Copy the connection string
7. Update your `.env` file

**Free Tier:**
- 5GB storage
- 1 billion row reads/month

---

### Option 4: CockroachDB (PostgreSQL-compatible)
**Best for:** Distributed database, high availability

#### Steps:
1. Go to [cockroachlabs.com](https://www.cockroachlabs.com)
2. Sign up for free
3. Create a cluster
4. Download the CA certificate
5. Get connection string
6. Update your `.env` file

**Free Tier:**
- 5GB storage
- Unlimited requests

---

## Setup Instructions

### 1. Update Your `.env` File

Create or update the `.env` file in your project root:

```env
# For PostgreSQL (Supabase, Railway, CockroachDB)
DATABASE_URL=postgresql://username:password@host:port/database

# For MySQL (PlanetScale, Railway)
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# Example for Supabase:
# DATABASE_URL=postgresql://postgres:your-password@db.xxx.supabase.co:5432/postgres

# Secret key for Flask
SECRET_KEY=your-secret-key-here-change-this
```

### 2. Install Required Packages

Run this command to install PostgreSQL support:

```bash
pip install -r requirements.txt
```

### 3. Initialize the Database

Run the app once to create all tables:

```bash
python app.py
```

Or use the migration script:

```bash
python migrate_to_online.py
```

### 4. Deploy Your Application (Optional)

To make your app accessible online, deploy it to:

#### **Render** (Recommended - Free)
1. Go to [render.com](https://render.com)
2. Connect your GitHub repository
3. Create a new Web Service
4. Set environment variables (DATABASE_URL, SECRET_KEY)
5. Deploy!

#### **Railway**
1. Already have your database there
2. Just add your app as a new service
3. Connect GitHub repo
4. Deploy automatically

#### **Heroku**
1. Install Heroku CLI
2. Run: `heroku create your-app-name`
3. Set config vars: `heroku config:set DATABASE_URL=...`
4. Deploy: `git push heroku main`

---

## Configuration Changes Made

The following files have been updated to support online databases:

1. **config.py** - Now supports both MySQL and PostgreSQL
2. **requirements.txt** - Added PostgreSQL driver (psycopg2-binary)
3. **.env.example** - Template for environment variables
4. **migrate_to_online.py** - Script to help migrate existing data

---

## Sharing with Friends

### If you deploy the app online:
1. Share the deployed URL (e.g., `https://your-app.onrender.com`)
2. Friends can access from anywhere
3. Everyone uses the same database

### If running locally but want shared database:
1. Use an online database (follow steps above)
2. Share the `.env` file with DATABASE_URL (keep it private!)
3. Each friend runs the app locally but connects to the same online database
4. **Security Note:** Don't share database credentials publicly!

---

## Troubleshooting

### Connection Error
- Check if database URL is correct
- Ensure your IP is whitelisted (some services require this)
- Verify username/password

### SSL Certificate Error (PostgreSQL)
Add `?sslmode=require` to your DATABASE_URL:
```
postgresql://user:pass@host:port/db?sslmode=require
```

### Migration Issues
- Make sure old database is backed up
- Run `python reset_db.py` to recreate tables
- Check logs for specific errors

---

## Security Best Practices

1. **Never commit `.env` file to Git**
   - Already in `.gitignore`
   - Share credentials securely (encrypted message, password manager)

2. **Use strong passwords**
   - Database password
   - SECRET_KEY in .env

3. **Limit database access**
   - Only share with trusted friends
   - Use read-only credentials for viewers

4. **Regular backups**
   - Most services provide automatic backups
   - Export data periodically

---

## Need Help?

- Check the service's documentation
- Look at error logs in terminal
- Verify environment variables are set correctly
- Test connection with a simple script

Good luck with your online database migration! 🚀
