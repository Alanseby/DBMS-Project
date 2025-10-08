from app import app, db
from models import User, Project, Bid, FreelancerProfile, Milestone, Review
from werkzeug.security import generate_password_hash
from datetime import datetime, date, UTC
from sqlalchemy import text

def reset_database():
    with app.app_context():
        # Disable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=0'))
        db.session.commit()
        
        db.drop_all()
        db.create_all()
        
        # Re-enable foreign key checks
        db.session.execute(text('SET FOREIGN_KEY_CHECKS=1'))
        db.session.commit()

        print("Creating sample data...")

        # Create users
        client = User(
            Name='Alice Client',
            Email='alice@example.com',
            Password=generate_password_hash('alice123'),
            Role='client',
            CreatedAt=datetime.now(UTC)
        )
        freelancer = User(
            Name='Bob Freelancer',
            Email='bob@example.com',
            Password=generate_password_hash('bob123'),
            Role='freelancer',
            CreatedAt=datetime.now(UTC)
        )
        admin = User(
            Name='Charlie Admin',
            Email='charlie@example.com',
            Password=generate_password_hash('charlie123'),
            Role='admin',
            CreatedAt=datetime.now(UTC)
        )
        db.session.add_all([client, freelancer, admin])
        db.session.commit()

        # Create freelancer profile
        profile = FreelancerProfile(
            FreelancerID=freelancer.UserID,
            Skills='Python, Flask, SQL, JavaScript',
            Experience='3 years experience in web development',  # Changed from Bio to Experience
            PortfolioURL='http://portfolio-bob.com'
        )
        db.session.add(profile)
        db.session.commit()

        # Create project
        project = Project(
            ClientID=client.UserID,
            Title='Build a Freelance Management System',
            Description='A system to manage projects, bids, and reviews.',
            Budget=5000.00,
            Status='open',
            CreatedAt=datetime.now(UTC)
        )
        db.session.add(project)
        db.session.commit()

        # Create bid
        bid = Bid(
            ProjectID=project.ProjectID,
            FreelancerID=freelancer.UserID,
            BidAmount=4500.00,
            CoverLetter='I have built similar systems before and can deliver quality.',
            Status='pending',
            BidDate=datetime.now(UTC)
        )
        db.session.add(bid)
        db.session.commit()

        # Create milestones
        milestones = [
            Milestone(
                ProjectID=project.ProjectID,
                Title='Database Design',
                Description='Design and implement database schema',
                Status='pending',
                DueDate=date(2025, 10, 15),
                Amount=1000.00
            ),
            Milestone(
                ProjectID=project.ProjectID,
                Title='Backend Development',
                Description='Implement API endpoints and business logic',
                Status='pending',
                DueDate=date(2025, 10, 30),
                Amount=2000.00
            ),
            Milestone(
                ProjectID=project.ProjectID,
                Title='Frontend Development',
                Description='Build user interface and integration',
                Status='pending',
                DueDate=date(2025, 11, 15),
                Amount=1500.00
            )
        ]
        db.session.add_all(milestones)
        db.session.commit()

        # Create review
        review = Review(
            ReviewerID=client.UserID,
            RevieweeID=freelancer.UserID,
            ProjectID=project.ProjectID,
            Rating=5,
            Comment='Great work, delivered on time!',
            CreatedAt=datetime.now(UTC)  # Changed from utcnow()
        )
        db.session.add(review)
        db.session.commit()

        print("✅ Database reset successfully!")
        print("\nSample users created:")
        print("Client: alice@example.com / alice123")
        print("Freelancer: bob@example.com / bob123")
        print("Admin: charlie@example.com / charlie123")

if __name__ == '__main__':
    reset_database()