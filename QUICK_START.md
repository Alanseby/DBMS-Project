# Quick Start Guide - Online Database Setup

## 🚀 Fastest Way to Get Started (Recommended: Supabase)

### Step 1: Create Online Database (5 minutes)

1. **Go to Supabase**: https://supabase.com
2. **Sign up** with GitHub or Google
3. **Create New Project**:
   - Name: `fprms-database`
   - Password: Create a strong password (save it!)
   - Region: Choose closest to you
4. **Wait 2-3 minutes** for setup

### Step 2: Get Your Database URL

1. In Supabase dashboard, go to **Settings** → **Database**
2. Scroll to **Connection String** section
3. Click **URI** tab
4. Copy the connection string (looks like this):
   ```
   postgresql://postgres:[YOUR-PASSWORD]@db.xxx.supabase.co:5432/postgres
   ```
5. Replace `[YOUR-PASSWORD]` with your actual password

### Step 3: Configure Your Project

1. **Copy the example environment file**:
   ```bash
   copy .env.example .env
   ```
   (On Mac/Linux use: `cp .env.example .env`)

2. **Edit `.env` file** and update:
   ```env
   DATABASE_URL=postgresql://postgres:your-password@db.xxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-here
   ```

### Step 4: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 5: Initialize Database

Run the migration script:
```bash
python migrate_to_online.py
```

This will:
- ✅ Verify your database connection
- ✅ Create all necessary tables
- ✅ Optionally create sample data for testing

### Step 6: Run Your App

```bash
python app.py
```

Open your browser: http://localhost:5000

---

## 👥 Sharing with Friends

### Option A: Share Database Only (Friends run locally)

1. **Share your `.env` file** with friends (via secure method)
2. Friends copy it to their project folder
3. Friends run: `pip install -r requirements.txt`
4. Friends run: `python app.py`
5. Everyone connects to the same database! 🎉

**Security Note**: Only share with trusted friends. Anyone with the DATABASE_URL can access your data.

### Option B: Deploy Online (Recommended for Multiple Users)

Deploy your entire app so friends can access via URL:

#### Using Render (Free):

1. **Push code to GitHub** (if not already)
2. Go to https://render.com
3. **Sign up** and click "New +" → "Web Service"
4. **Connect your GitHub repository**
5. **Configure**:
   - Name: `fprms-app`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
6. **Add Environment Variables**:
   - `DATABASE_URL`: (your Supabase URL)
   - `SECRET_KEY`: (generate a random string)
7. **Deploy!**

Your app will be live at: `https://fprms-app.onrender.com`

Share this URL with friends - no setup needed on their end!

---

## 🔧 Troubleshooting

### "Connection refused" or "Can't connect to database"

**Fix**:
1. Check your DATABASE_URL in `.env` is correct
2. Ensure password doesn't have special characters (or URL-encode them)
3. Verify your database is running (check Supabase dashboard)

### "No module named 'psycopg2'"

**Fix**:
```bash
pip install -r requirements.txt
```

### "Table doesn't exist"

**Fix**:
```bash
python migrate_to_online.py
```

### SSL Certificate Error

**Fix**: Add `?sslmode=require` to your DATABASE_URL:
```env
DATABASE_URL=postgresql://user:pass@host:5432/db?sslmode=require
```

---

## 📊 Database Providers Comparison

| Provider | Type | Free Tier | Best For |
|----------|------|-----------|----------|
| **Supabase** | PostgreSQL | 500MB, Unlimited requests | Beginners, Easy setup |
| **Railway** | PostgreSQL/MySQL | $5/month credit | Quick deployment |
| **PlanetScale** | MySQL | 5GB, 1B reads/month | MySQL users |
| **Render** | PostgreSQL | 90 days free | App + DB together |

---

## 🎯 What You've Accomplished

✅ Migrated from local to online database  
✅ Your app can now be accessed by multiple users  
✅ Database is backed up automatically  
✅ Friends can collaborate on the same data  
✅ Ready for deployment to production  

---

## 📚 Additional Resources

- **Full Setup Guide**: See `ONLINE_DATABASE_SETUP.md`
- **Supabase Docs**: https://supabase.com/docs
- **Flask Deployment**: https://flask.palletsprojects.com/en/2.3.x/deploying/

---

## 🆘 Need Help?

1. Check error messages carefully
2. Verify `.env` file is in the project root
3. Ensure all dependencies are installed
4. Check database dashboard for connection issues

**Common Issues**:
- Forgot to copy `.env.example` to `.env`
- Wrong password in DATABASE_URL
- Didn't run `pip install -r requirements.txt`
- Database not initialized (run `migrate_to_online.py`)

Good luck! 🚀
