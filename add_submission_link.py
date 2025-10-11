"""
Migration script to add SubmissionLink column to Milestones table
Run this script once to update your existing database
"""
from app import app, db
from sqlalchemy import text, inspect

def add_submission_link_column():
    with app.app_context():
        try:
            # Use SQLAlchemy inspector to check columns (works for all databases)
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('Milestones')]
            
            if 'SubmissionLink' not in columns:
                # Add the new column
                with db.engine.connect() as conn:
                    conn.execute(text("ALTER TABLE Milestones ADD COLUMN SubmissionLink VARCHAR(500)"))
                    conn.commit()
                print("✅ Successfully added SubmissionLink column to Milestones table")
            else:
                print("ℹ️  SubmissionLink column already exists")
        except Exception as e:
            print(f"❌ Error: {e}")
            print("\nAlternatively, you can run this SQL directly in your MySQL database:")
            print("ALTER TABLE Milestones ADD COLUMN SubmissionLink VARCHAR(500);")

if __name__ == '__main__':
    add_submission_link_column()
