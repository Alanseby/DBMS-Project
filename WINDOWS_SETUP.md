# Windows Setup Guide

## ✅ Fixed: PostgreSQL Driver Issue

The original `psycopg2-binary` package has build issues on Windows. I've replaced it with **pg8000**, a pure Python PostgreSQL driver that works perfectly on Windows without requiring PostgreSQL to be installed.

## 📦 Installation Steps

### 1. Install Dependencies

Open Command Prompt or PowerShell in your project folder and run:

```bash
pip install -r requirements.txt
```

This will install:
- Flask and extensions
- PyMySQL (for MySQL)
- **pg8000** (for PostgreSQL - Windows compatible!)
- gunicorn (for deployment)

### 2. Verify Installation

Check if pg8000 is installed:

```bash
pip list | findstr pg8000
```

You should see: `pg8000  1.30.3`

## 🔧 Database URL Format

### For PostgreSQL (Supabase, Railway, etc.):

Use `postgresql+pg8000://` instead of `postgresql://`

```env
# In your .env file:
DATABASE_URL=postgresql+pg8000://username:password@host:port/database

# Example for Supabase:
DATABASE_URL=postgresql+pg8000://postgres:yourpassword@db.xxx.supabase.co:5432/postgres
```

### For MySQL (Local or PlanetScale):

```env
DATABASE_URL=mysql+pymysql://username:password@host:port/database

# Example for local MySQL:
DATABASE_URL=mysql+pymysql://fprms_user:fprms_pass@localhost/fprms
```

## 🚀 Quick Start

### Option 1: Using MySQL (Local)

1. **Install MySQL** (if not already installed)
2. **Create database**:
   ```sql
   CREATE DATABASE fprms;
   CREATE USER 'fprms_user'@'localhost' IDENTIFIED BY 'fprms_pass';
   GRANT ALL PRIVILEGES ON fprms.* TO 'fprms_user'@'localhost';
   FLUSH PRIVILEGES;
   ```
3. **Copy environment file**:
   ```bash
   copy .env.example .env
   ```
4. **Run the app**:
   ```bash
   python app.py
   ```

### Option 2: Using PostgreSQL (Supabase - Online)

1. **Create Supabase account**: https://supabase.com
2. **Create new project** and get connection string
3. **Copy environment file**:
   ```bash
   copy .env.example .env
   ```
4. **Edit `.env`** and add:
   ```env
   DATABASE_URL=postgresql+pg8000://postgres:yourpassword@db.xxx.supabase.co:5432/postgres
   SECRET_KEY=your-secret-key-here
   ```
5. **Initialize database**:
   ```bash
   python migrate_to_online.py
   ```
6. **Run the app**:
   ```bash
   python app.py
   ```

## 🐛 Troubleshooting

### Error: "No module named 'pg8000'"

**Solution**:
```bash
pip install pg8000==1.30.3
```

### Error: "Can't connect to database"

**For PostgreSQL**:
- Ensure you're using `postgresql+pg8000://` (not just `postgresql://`)
- Check password doesn't have special characters (or URL-encode them)
- Verify the connection string is correct

**For MySQL**:
- Ensure MySQL server is running
- Check credentials are correct
- Verify database exists

### Error: "No such table"

**Solution**:
```bash
python migrate_to_online.py
```

Or manually create tables:
```bash
python
>>> from app import app, db
>>> with app.app_context():
...     db.create_all()
>>> exit()
```

### Error: "Access denied for user"

**For MySQL**:
```sql
-- Run in MySQL:
GRANT ALL PRIVILEGES ON fprms.* TO 'fprms_user'@'localhost';
FLUSH PRIVILEGES;
```

## 📝 What Changed?

### Before (Didn't work on Windows):
```txt
psycopg2-binary==2.9.9  # ❌ Requires PostgreSQL installation
```

### After (Works on Windows):
```txt
pg8000==1.30.3  # ✅ Pure Python, no dependencies
```

## 🔄 Automatic Driver Detection

The `config.py` has been updated to automatically use pg8000 for PostgreSQL connections. You can use either format in your `.env`:

```env
# Both of these work:
DATABASE_URL=postgresql://user:pass@host:5432/db
DATABASE_URL=postgresql+pg8000://user:pass@host:5432/db
```

The config will automatically convert to use pg8000!

## 🎯 Recommended for Windows Users

**Best Option**: Use **Supabase** (PostgreSQL online)
- No local PostgreSQL installation needed
- Free tier is generous
- Works perfectly with pg8000
- Easy to share with friends

**Alternative**: Use **MySQL locally**
- If you already have MySQL installed
- Good for offline development

## 📚 Additional Resources

- **pg8000 Documentation**: https://github.com/tlocke/pg8000
- **Supabase Setup**: See `QUICK_START.md`
- **Full Guide**: See `ONLINE_DATABASE_SETUP.md`

## ✨ You're All Set!

The PostgreSQL driver issue is now fixed. You can proceed with:

1. **Install dependencies**: `pip install -r requirements.txt`
2. **Setup database**: Follow Option 1 or 2 above
3. **Run the app**: `python app.py`

No more build errors! 🎉
