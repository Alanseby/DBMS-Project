"""
Database Reset Script with Sample Data
This script will drop all tables, recreate them, and populate with sample data
"""

from app import app, db
from models import User, Project, Bid, FreelancerProfile, Milestone, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, timedelta

def reset_database():
    with app.app_context():
        print("🔄 Resetting database...")
        
        try:
            # Disable foreign key checks to allow dropping tables with constraints
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 0"))
            db.session.commit()
            
            # Get all table names from the database
            result = db.session.execute(db.text("SHOW TABLES"))
            tables = [row[0] for row in result]
            
            # Drop each table individually
            for table in tables:
                print(f"   Dropping table: {table}")
                db.session.execute(db.text(f"DROP TABLE IF EXISTS `{table}`"))
            
            db.session.commit()
            print("✅ Dropped all tables")
            
            # Re-enable foreign key checks
            db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
            db.session.commit()
            
        except Exception as e:
            print(f"❌ Error during table drop: {e}")
            db.session.rollback()
            # Try to re-enable foreign key checks even if there was an error
            try:
                db.session.execute(db.text("SET FOREIGN_KEY_CHECKS = 1"))
                db.session.commit()
            except:
                pass
            raise
        
        # Create all tables
        db.create_all()
        print("✅ Created all tables")
        
        # Create sample users
        print("\n👥 Creating sample users...")
        
        # Admin user
        admin = User(
            Name="Admin User",
            Email="admin@example.com",
            Password=generate_password_hash("admin123"),
            Role="admin"
        )
        db.session.add(admin)
        
        # Client users
        client1 = User(
            Name="John Smith",
            Email="john@example.com",
            Password=generate_password_hash("client123"),
            Role="client"
        )
        db.session.add(client1)
        
        client2 = User(
            Name="Sarah Johnson",
            Email="sarah@example.com",
            Password=generate_password_hash("client123"),
            Role="client"
        )
        db.session.add(client2)
        
        # Freelancer users
        freelancer1 = User(
            Name="Alice Developer",
            Email="alice@example.com",
            Password=generate_password_hash("freelancer123"),
            Role="freelancer"
        )
        db.session.add(freelancer1)
        
        freelancer2 = User(
            Name="Bob Designer",
            Email="bob@example.com",
            Password=generate_password_hash("freelancer123"),
            Role="freelancer"
        )
        db.session.add(freelancer2)
        
        freelancer3 = User(
            Name="Charlie Coder",
            Email="charlie@example.com",
            Password=generate_password_hash("freelancer123"),
            Role="freelancer"
        )
        db.session.add(freelancer3)
        
        db.session.commit()
        print(f"✅ Created {User.query.count()} users")
        
        # Create freelancer profiles
        print("\n💼 Creating freelancer profiles...")
        
        profile1 = FreelancerProfile(
            FreelancerID=freelancer1.UserID,
            Skills="Python, Flask, Django, React, JavaScript, SQL",
            Experience="5 years of full-stack development experience. Specialized in web applications and APIs.",
            PortfolioURL="https://github.com/alicedev"
        )
        db.session.add(profile1)
        
        profile2 = FreelancerProfile(
            FreelancerID=freelancer2.UserID,
            Skills="UI/UX Design, Figma, Adobe XD, Photoshop, HTML/CSS",
            Experience="3 years of design experience. Expert in creating modern and user-friendly interfaces.",
            PortfolioURL="https://behance.net/bobdesigner"
        )
        db.session.add(profile2)
        
        profile3 = FreelancerProfile(
            FreelancerID=freelancer3.UserID,
            Skills="Java, Spring Boot, Microservices, Docker, Kubernetes",
            Experience="4 years of backend development. Focused on scalable enterprise solutions.",
            PortfolioURL="https://github.com/charliecoder"
        )
        db.session.add(profile3)
        
        db.session.commit()
        print(f"✅ Created {FreelancerProfile.query.count()} freelancer profiles")
        
        # Create sample projects
        print("\n📋 Creating sample projects...")
        
        project1 = Project(
            ClientID=client1.UserID,
            Title="E-commerce Website Development",
            Description="Need a full-featured e-commerce website with payment integration, product catalog, and admin dashboard.",
            Budget=5000.00,
            Status="open",
            CreatedAt=datetime.utcnow() - timedelta(days=5)
        )
        db.session.add(project1)
        
        project2 = Project(
            ClientID=client1.UserID,
            Title="Mobile App UI/UX Design",
            Description="Looking for a talented designer to create modern UI/UX for our fitness tracking mobile app.",
            Budget=2000.00,
            Status="in_progress",
            CreatedAt=datetime.utcnow() - timedelta(days=10)
        )
        db.session.add(project2)
        
        project3 = Project(
            ClientID=client2.UserID,
            Title="REST API Development",
            Description="Need a RESTful API for our inventory management system with authentication and documentation.",
            Budget=3000.00,
            Status="open",
            CreatedAt=datetime.utcnow() - timedelta(days=3)
        )
        db.session.add(project3)
        
        project4 = Project(
            ClientID=client2.UserID,
            Title="Website Redesign",
            Description="Complete redesign of our company website with modern look and responsive design.",
            Budget=2500.00,
            Status="completed",
            CreatedAt=datetime.utcnow() - timedelta(days=30)
        )
        db.session.add(project4)
        
        db.session.commit()
        print(f"✅ Created {Project.query.count()} projects")
        
        # Create sample bids
        print("\n💰 Creating sample bids...")
        
        # Bids for project 1 (open)
        bid1 = Bid(
            ProjectID=project1.ProjectID,
            FreelancerID=freelancer1.UserID,
            BidAmount=4500.00,
            CoverLetter="I have extensive experience in e-commerce development. I can deliver a high-quality solution within your budget.",
            Status="pending",
            BidDate=datetime.utcnow() - timedelta(days=4)
        )
        db.session.add(bid1)
        
        bid2 = Bid(
            ProjectID=project1.ProjectID,
            FreelancerID=freelancer3.UserID,
            BidAmount=4800.00,
            CoverLetter="I specialize in building scalable e-commerce platforms. Let me help you create an amazing online store.",
            Status="pending",
            BidDate=datetime.utcnow() - timedelta(days=3)
        )
        db.session.add(bid2)
        
        # Bids for project 2 (in progress - one accepted)
        bid3 = Bid(
            ProjectID=project2.ProjectID,
            FreelancerID=freelancer2.UserID,
            BidAmount=1800.00,
            CoverLetter="I'm a UI/UX designer with a passion for creating beautiful and intuitive mobile interfaces.",
            Status="accepted",
            BidDate=datetime.utcnow() - timedelta(days=9)
        )
        db.session.add(bid3)
        
        bid4 = Bid(
            ProjectID=project2.ProjectID,
            FreelancerID=freelancer1.UserID,
            BidAmount=2000.00,
            CoverLetter="I can provide both design and development services for your mobile app.",
            Status="rejected",
            BidDate=datetime.utcnow() - timedelta(days=9)
        )
        db.session.add(bid4)
        
        # Bids for project 3 (open)
        bid5 = Bid(
            ProjectID=project3.ProjectID,
            FreelancerID=freelancer1.UserID,
            BidAmount=2800.00,
            CoverLetter="I have built numerous REST APIs with comprehensive documentation. I use Flask and FastAPI.",
            Status="pending",
            BidDate=datetime.utcnow() - timedelta(days=2)
        )
        db.session.add(bid5)
        
        bid6 = Bid(
            ProjectID=project3.ProjectID,
            FreelancerID=freelancer3.UserID,
            BidAmount=2900.00,
            CoverLetter="Expert in Spring Boot and microservices. I can deliver a robust and well-documented API.",
            Status="pending",
            BidDate=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(bid6)
        
        # Bid for project 4 (completed - accepted)
        bid7 = Bid(
            ProjectID=project4.ProjectID,
            FreelancerID=freelancer2.UserID,
            BidAmount=2300.00,
            CoverLetter="I can redesign your website with a modern, responsive design that looks great on all devices.",
            Status="accepted",
            BidDate=datetime.utcnow() - timedelta(days=29)
        )
        db.session.add(bid7)
        
        db.session.commit()
        print(f"✅ Created {Bid.query.count()} bids")
        
        # Create milestones for in-progress project
        print("\n🎯 Creating sample milestones...")
        
        milestone1 = Milestone(
            ProjectID=project2.ProjectID,
            Title="Initial Wireframes",
            Description="Create low-fidelity wireframes for all main screens",
            Status="completed",
            DueDate=(datetime.utcnow() - timedelta(days=5)).date(),
            SubmissionLink="https://figma.com/wireframes-v1"
        )
        db.session.add(milestone1)
        
        milestone2 = Milestone(
            ProjectID=project2.ProjectID,
            Title="High-Fidelity Mockups",
            Description="Design high-fidelity mockups with colors and branding",
            Status="submitted",
            DueDate=(datetime.utcnow() + timedelta(days=2)).date(),
            SubmissionLink="https://figma.com/mockups-v1"
        )
        db.session.add(milestone2)
        
        milestone3 = Milestone(
            ProjectID=project2.ProjectID,
            Title="Interactive Prototype",
            Description="Create clickable prototype for user testing",
            Status="pending",
            DueDate=(datetime.utcnow() + timedelta(days=7)).date()
        )
        db.session.add(milestone3)
        
        # Milestones for completed project
        milestone4 = Milestone(
            ProjectID=project4.ProjectID,
            Title="Homepage Redesign",
            Description="Redesign the homepage with new branding",
            Status="completed",
            DueDate=(datetime.utcnow() - timedelta(days=20)).date(),
            SubmissionLink="https://example.com/homepage-preview"
        )
        db.session.add(milestone4)
        
        milestone5 = Milestone(
            ProjectID=project4.ProjectID,
            Title="Inner Pages Redesign",
            Description="Redesign all inner pages and ensure consistency",
            Status="completed",
            DueDate=(datetime.utcnow() - timedelta(days=10)).date(),
            SubmissionLink="https://example.com/pages-preview"
        )
        db.session.add(milestone5)
        
        db.session.commit()
        print(f"✅ Created {Milestone.query.count()} milestones")
        
        # Create sample reviews
        print("\n⭐ Creating sample reviews...")
        
        review1 = Review(
            ProjectID=project4.ProjectID,
            ReviewerID=client2.UserID,
            RevieweeID=freelancer2.UserID,
            Rating=5,
            Comment="Excellent work! Bob delivered a beautiful design that exceeded our expectations. Highly recommended!",
            CreatedAt=datetime.utcnow() - timedelta(days=2)
        )
        db.session.add(review1)
        
        review2 = Review(
            ProjectID=project4.ProjectID,
            ReviewerID=freelancer2.UserID,
            RevieweeID=client2.UserID,
            Rating=5,
            Comment="Great client to work with! Clear communication and prompt feedback throughout the project.",
            CreatedAt=datetime.utcnow() - timedelta(days=1)
        )
        db.session.add(review2)
        
        db.session.commit()
        print(f"✅ Created {Review.query.count()} reviews")
        
        # Print summary
        print("\n" + "="*60)
        print("✅ DATABASE RESET COMPLETE!")
        print("="*60)
        print("\n📊 Summary:")
        print(f"   • Users: {User.query.count()}")
        print(f"   • Freelancer Profiles: {FreelancerProfile.query.count()}")
        print(f"   • Projects: {Project.query.count()}")
        print(f"   • Bids: {Bid.query.count()}")
        print(f"   • Milestones: {Milestone.query.count()}")
        print(f"   • Reviews: {Review.query.count()}")
        
        print("\n🔑 Login Credentials:")
        print("   Admin:")
        print("      Email: admin@example.com")
        print("      Password: admin123")
        print("\n   Clients:")
        print("      Email: john@example.com | Password: client123")
        print("      Email: sarah@example.com | Password: client123")
        print("\n   Freelancers:")
        print("      Email: alice@example.com | Password: freelancer123")
        print("      Email: bob@example.com | Password: freelancer123")
        print("      Email: charlie@example.com | Password: freelancer123")
        print("\n" + "="*60)

if __name__ == '__main__':
    reset_database()
