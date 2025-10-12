"""
Migration script to transfer data from local database to online database
or to initialize a new online database with the correct schema.
"""

import os
from app import app, db
from models import User, Project, Bid, FreelancerProfile, Milestone, Review

def initialize_database():
    """Create all tables in the online database"""
    print("🔧 Initializing database schema...")
    
    with app.app_context():
        # Drop all existing tables (use with caution!)
        # db.drop_all()
        
        # Create all tables
        db.create_all()
        print("✅ Database tables created successfully!")
        
        # Verify tables
        inspector = db.inspect(db.engine)
        tables = inspector.get_table_names()
        print(f"\n📊 Created tables: {', '.join(tables)}")
        
        return True

def create_sample_data():
    """Create sample data for testing"""
    print("\n🌱 Creating sample data...")
    
    with app.app_context():
        # Check if data already exists
        if User.query.first():
            print("⚠️  Database already contains data. Skipping sample data creation.")
            return
        
        from werkzeug.security import generate_password_hash
        
        # Create admin user
        admin = User(
            Name="Admin User",
            Email="admin@fprms.com",
            Password=generate_password_hash("admin123"),
            Role="admin"
        )
        db.session.add(admin)
        
        # Create client user
        client = User(
            Name="John Client",
            Email="client@fprms.com",
            Password=generate_password_hash("client123"),
            Role="client"
        )
        db.session.add(client)
        
        # Create freelancer user
        freelancer = User(
            Name="Jane Freelancer",
            Email="freelancer@fprms.com",
            Password=generate_password_hash("freelancer123"),
            Role="freelancer"
        )
        db.session.add(freelancer)
        
        db.session.commit()
        
        # Create freelancer profile
        profile = FreelancerProfile(
            FreelancerID=freelancer.UserID,
            Skills="Python, Flask, Web Development",
            Experience="5 years of experience in web development",
            PortfolioURL="https://github.com/janefreelancer"
        )
        db.session.add(profile)
        
        # Create sample project
        project = Project(
            ClientID=client.UserID,
            Title="Build a Web Application",
            Description="Need a full-stack web application with user authentication",
            Budget=5000.00,
            Status="open"
        )
        db.session.add(project)
        
        db.session.commit()
        
        print("✅ Sample data created successfully!")
        print("\n📝 Sample Login Credentials:")
        print("   Admin:      admin@fprms.com / admin123")
        print("   Client:     client@fprms.com / client123")
        print("   Freelancer: freelancer@fprms.com / freelancer123")

def verify_connection():
    """Verify database connection"""
    print("🔍 Verifying database connection...")
    
    try:
        with app.app_context():
            # Try to connect
            db.engine.connect()
            print("✅ Database connection successful!")
            
            # Get database info
            db_url = app.config['SQLALCHEMY_DATABASE_URI']
            
            # Hide password in output
            if '@' in db_url:
                parts = db_url.split('@')
                user_part = parts[0].split('://')[1].split(':')[0]
                host_part = '@'.join(parts[1:])
                safe_url = f"...://{user_part}:****@{host_part}"
            else:
                safe_url = db_url
            
            print(f"📍 Connected to: {safe_url}")
            
            # Check if it's PostgreSQL or MySQL
            if 'postgresql' in db_url:
                print("🐘 Database type: PostgreSQL")
            elif 'mysql' in db_url:
                print("🐬 Database type: MySQL")
            else:
                print("❓ Database type: Unknown")
            
            return True
            
    except Exception as e:
        print(f"❌ Database connection failed: {str(e)}")
        print("\n💡 Tips:")
        print("   1. Check your DATABASE_URL in .env file")
        print("   2. Ensure the database server is running")
        print("   3. Verify your credentials are correct")
        print("   4. Check if your IP is whitelisted (for cloud databases)")
        return False

def main():
    """Main migration function"""
    print("=" * 60)
    print("🚀 FPRMS Database Migration Tool")
    print("=" * 60)
    
    # Step 1: Verify connection
    if not verify_connection():
        return
    
    print("\n" + "=" * 60)
    
    # Step 2: Initialize database
    if not initialize_database():
        return
    
    print("\n" + "=" * 60)
    
    # Step 3: Ask about sample data
    response = input("\n❓ Do you want to create sample data for testing? (y/n): ").lower()
    if response == 'y':
        create_sample_data()
    
    print("\n" + "=" * 60)
    print("✨ Migration completed successfully!")
    print("=" * 60)
    print("\n📌 Next steps:")
    print("   1. Run your app: python app.py")
    print("   2. Open browser: http://localhost:5000")
    print("   3. Share your DATABASE_URL with friends (keep it secure!)")
    print("\n🔒 Security reminder:")
    print("   - Never commit .env file to Git")
    print("   - Use strong passwords")
    print("   - Only share credentials with trusted people")
    print("\n")

if __name__ == "__main__":
    main()
