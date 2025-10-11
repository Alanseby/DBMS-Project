from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from models import db, User, Project, Bid, FreelancerProfile, Milestone, Review
from config import Config
from datetime import datetime

app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Context processor to make 'now' available in templates
@app.context_processor
def inject_now():
    return {'now': datetime.utcnow()}

# ========================
# AUTHENTICATION ROUTES
# ========================

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(Email=email).first()
        
        if user and check_password_hash(user.Password, password):
            login_user(user)
            flash('Login successful!', 'success')
            
            if user.Role == 'freelancer':
                return redirect(url_for('freelancer_dashboard'))
            elif user.Role == 'client':
                return redirect(url_for('client_dashboard'))
            else:
                return redirect(url_for('admin_dashboard'))
        else:
            flash('Invalid email or password!', 'error')
    
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        role = request.form['role']
        
        if User.query.filter_by(Email=email).first():
            flash('Email already registered!', 'error')
            return redirect(url_for('register'))
        
        hashed_password = generate_password_hash(password)
        new_user = User(Name=name, Email=email, Password=hashed_password, Role=role)
        
        db.session.add(new_user)
        db.session.commit()
        
        if role == 'freelancer':
            freelancer_profile = FreelancerProfile(
                FreelancerID=new_user.UserID,
                Skills=request.form.get('skills', ''),
                Experience=request.form.get('experience', ''),
                PortfolioURL=request.form.get('portfolio_url', '')
            )
            db.session.add(freelancer_profile)
            db.session.commit()
        
        flash('Registration successful! Please login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ========================
# DASHBOARD ROUTES
# ========================

@app.route('/dashboard/freelancer')
@login_required
def freelancer_dashboard():
    if current_user.Role != 'freelancer':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    # Get freelancer's bids and projects
    bids = Bid.query.filter_by(FreelancerID=current_user.UserID).all()
    open_projects = Project.query.filter_by(Status='open').all()
    
    return render_template('dashboard/freelancer.html', 
                         bids=bids, 
                         open_projects=open_projects)

@app.route('/dashboard/client')
@login_required
def client_dashboard():
    if current_user.Role != 'client':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    projects = Project.query.filter_by(ClientID=current_user.UserID).all()
    active_projects = [p for p in projects if p.Status in ['open', 'in_progress']]
    completed_projects = [p for p in projects if p.Status == 'completed']
    
    return render_template('dashboard/client.html', 
                         projects=projects,
                         active_projects=active_projects,
                         completed_projects=completed_projects)

@app.route('/dashboard/admin')
@login_required
def admin_dashboard():
    if current_user.Role != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    total_users = User.query.count()
    total_projects = Project.query.count()
    total_bids = Bid.query.count()
    recent_projects = Project.query.order_by(Project.CreatedAt.desc()).limit(5).all()
    
    return render_template('dashboard/admin.html',
                         total_users=total_users,
                         total_projects=total_projects,
                         total_bids=total_bids,
                         recent_projects=recent_projects)

# ========================
# PROJECT ROUTES
# ========================

@app.route('/projects')
@login_required
def view_projects():
    print("🔍 View Projects route called")  # Debug print
    projects = Project.query.filter_by(Status='open').all()
    print(f"📊 Found {len(projects)} open projects")  # Debug print
    return render_template('projects/view_projects.html', projects=projects)

@app.route('/projects/create', methods=['GET', 'POST'])
@login_required
def create_project():
    if current_user.Role != 'client':
        flash('Only clients can create projects!', 'error')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        budget = request.form['budget']
        
        new_project = Project(
            ClientID=current_user.UserID,
            Title=title,
            Description=description,
            Budget=budget
        )
        
        db.session.add(new_project)
        db.session.commit()
        flash('Project created successfully!', 'success')
        return redirect(url_for('client_dashboard'))
    
    return render_template('projects/create_project.html')

@app.route('/projects/<int:project_id>')
@login_required
def project_details(project_id):
    project = Project.query.get_or_404(project_id)
    bids = Bid.query.filter_by(ProjectID=project_id).all()
    milestones = Milestone.query.filter_by(ProjectID=project_id).all()

    # Order milestones by creation order
    milestones = Milestone.query.filter_by(ProjectID=project_id).order_by(Milestone.MilestoneID).all()
    
    # Compute progress based on milestone count
    progress = 0
    if milestones:
        completed_milestones = [m for m in milestones if m.Status == 'completed']
        progress = int((len(completed_milestones) / len(milestones)) * 100)

    # Find next milestone that can be completed (first non-completed one)
    next_completable_milestone_id = None
    if milestones:
        for milestone in milestones:
            if milestone.Status != 'completed':
                next_completable_milestone_id = milestone.MilestoneID
                break

    # Check if current user has already bid on this project
    user_bid = None
    if current_user.Role == 'freelancer':
        user_bid = Bid.query.filter_by(
            ProjectID=project_id,
            FreelancerID=current_user.UserID
        ).first()

    # Authorization flag for milestone status updates
    can_update_milestones = False
    if current_user.UserID == project.ClientID:
        can_update_milestones = True
    elif current_user.Role == 'freelancer':
        accepted_bid = Bid.query.filter_by(ProjectID=project.ProjectID, FreelancerID=current_user.UserID, Status='accepted').first()
        if accepted_bid:
            can_update_milestones = True

    # Calculate average ratings for each freelancer who bid
    freelancer_ratings = {}
    for bid in bids:
        reviews = Review.query.filter_by(RevieweeID=bid.FreelancerID).all()
        if reviews:
            avg_rating = sum(r.Rating for r in reviews) / len(reviews)
            freelancer_ratings[bid.FreelancerID] = {
                'average': round(avg_rating, 1),
                'count': len(reviews)
            }
        else:
            freelancer_ratings[bid.FreelancerID] = {
                'average': 0,
                'count': 0
            }

    # Get accepted freelancer and check if client has reviewed them
    accepted_freelancer = None
    client_review = None
    accepted_bid = Bid.query.filter_by(ProjectID=project_id, Status='accepted').first()
    if accepted_bid:
        accepted_freelancer = accepted_bid.freelancer
        # Check if client has already reviewed this freelancer for this project
        if current_user.UserID == project.ClientID:
            client_review = Review.query.filter_by(
                ProjectID=project_id,
                ReviewerID=current_user.UserID,
                RevieweeID=accepted_freelancer.UserID
            ).first()

    return render_template(
        'projects/project_details.html',
        project=project,
        bids=bids,
        milestones=milestones,
        progress=progress,
        can_update_milestones=can_update_milestones,
        next_completable_milestone_id=next_completable_milestone_id,
        user_bid=user_bid,
        freelancer_ratings=freelancer_ratings,
        accepted_freelancer=accepted_freelancer,
        client_review=client_review
    )

@app.route('/projects/<int:project_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if project.ClientID != current_user.UserID:
        flash('Access denied!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    if request.method == 'POST':
        project.Title = request.form['title']
        project.Description = request.form['description']
        project.Budget = request.form['budget']
        project.Status = request.form['status']
        
        db.session.commit()
        flash('Project updated successfully!', 'success')
        return redirect(url_for('project_details', project_id=project_id))
    
    return render_template('projects/edit_project.html', project=project)

@app.route('/projects/<int:project_id>/close')
@login_required
def close_project(project_id):
    project = Project.query.get_or_404(project_id)
    
    if project.ClientID != current_user.UserID:
        flash('Access denied!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    project.Status = 'completed'
    db.session.commit()
    
    flash('Project marked as completed!', 'success')
    return redirect(url_for('project_details', project_id=project_id))

# ========================
# BID MANAGEMENT ROUTES
# ========================

@app.route('/projects/<int:project_id>/bid', methods=['POST'])
@login_required
def place_bid(project_id):
    if current_user.Role != 'freelancer':
        flash('Only freelancers can place bids!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    bid_amount = request.form['bid_amount']
    cover_letter = request.form['cover_letter']
    
    existing_bid = Bid.query.filter_by(
        ProjectID=project_id, 
        FreelancerID=current_user.UserID
    ).first()
    
    if existing_bid:
        flash('You have already placed a bid on this project!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    new_bid = Bid(
        ProjectID=project_id,
        FreelancerID=current_user.UserID,
        BidAmount=bid_amount,
        CoverLetter=cover_letter
    )
    
    db.session.add(new_bid)
    db.session.commit()
    
    flash('Bid placed successfully!', 'success')
    return redirect(url_for('project_details', project_id=project_id))

@app.route('/bids')
@login_required
def my_bids():
    if current_user.Role != 'freelancer':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    bids = Bid.query.filter_by(FreelancerID=current_user.UserID).all()
    return render_template('bids/my_bids.html', bids=bids)

# Fixed: Removed duplicate route - keeping the better version
@app.route('/bids/<int:bid_id>/withdraw')
@login_required
def withdraw_bid(bid_id):
    if current_user.Role != 'freelancer':
        flash('Only freelancers can withdraw bids!', 'error')
        return redirect(url_for('index'))
    
    bid = Bid.query.get_or_404(bid_id)
    
    if bid.FreelancerID != current_user.UserID:
        flash('Access denied!', 'error')
        return redirect(url_for('my_bids'))
    
    if bid.Status != 'pending':
        flash('You can only withdraw pending bids!', 'error')
        return redirect(url_for('my_bids'))
    
    db.session.delete(bid)
    db.session.commit()
    
    flash('Bid withdrawn successfully!', 'success')
    return redirect(url_for('my_bids'))

@app.route('/projects/<int:project_id>/accept_bid/<int:bid_id>')
@login_required
def accept_bid(project_id, bid_id):
    project = Project.query.get_or_404(project_id)
    bid = Bid.query.get_or_404(bid_id)
    
    if project.ClientID != current_user.UserID:
        flash('Access denied!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    # Update project status
    project.Status = 'in_progress'
    
    # Update bid status
    bid.Status = 'accepted'
    
    # Reject all other bids for this project
    Bid.query.filter_by(ProjectID=project_id).filter(Bid.BidID != bid_id).update({'Status': 'rejected'})
    
    db.session.commit()
    
    flash('Bid accepted! Project is now in progress.', 'success')
    return redirect(url_for('project_details', project_id=project_id))

# ========================
# MILESTONE ROUTES
# ========================

@app.route('/projects/<int:project_id>/milestones/create', methods=['POST'])
@login_required
def create_milestones(project_id):
    project = Project.query.get_or_404(project_id)
    
    if project.ClientID != current_user.UserID:
        flash('Access denied!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    # Get all milestone data from form
    milestone_count = 0
    index = 0
    
    while True:
        title_key = f'milestones[{index}][title]'
        if title_key not in request.form:
            break
            
        title = request.form[title_key]
        description = request.form.get(f'milestones[{index}][description]', '')
        due_date = request.form[f'milestones[{index}][due_date]']
        
        milestone = Milestone(
            ProjectID=project_id,
            Title=title,
            Description=description,
            DueDate=datetime.strptime(due_date, '%Y-%m-%d').date(),
            Status='pending'
        )
        
        db.session.add(milestone)
        milestone_count += 1
        index += 1
    
    db.session.commit()
    
    flash(f'{milestone_count} milestone(s) created successfully!', 'success')
    return redirect(url_for('project_details', project_id=project_id))

@app.route('/milestones/<int:milestone_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_milestone(milestone_id):
    """Client edits a milestone"""
    milestone = Milestone.query.get_or_404(milestone_id)
    project = milestone.project
    
    # Only client can edit milestones
    if current_user.UserID != project.ClientID:
        flash('Only the client can edit milestones!', 'error')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    if request.method == 'POST':
        milestone.Title = request.form['title']
        milestone.Description = request.form.get('description', '')
        milestone.DueDate = datetime.strptime(request.form['due_date'], '%Y-%m-%d').date()
        
        db.session.commit()
        flash('✅ Milestone updated successfully!', 'success')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    return render_template('milestones/edit_milestone.html', milestone=milestone, project=project)

@app.route('/milestones/<int:milestone_id>/delete', methods=['POST'])
@login_required
def delete_milestone(milestone_id):
    """Client deletes a milestone"""
    milestone = Milestone.query.get_or_404(milestone_id)
    project = milestone.project
    
    # Only client can delete milestones
    if current_user.UserID != project.ClientID:
        flash('Only the client can delete milestones!', 'error')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    # Don't allow deletion of completed or submitted milestones
    if milestone.Status in ['submitted', 'completed']:
        flash('Cannot delete submitted or completed milestones!', 'warning')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    db.session.delete(milestone)
    db.session.commit()
    
    flash('🗑️ Milestone deleted successfully!', 'success')
    return redirect(url_for('project_details', project_id=project.ProjectID))

@app.route('/milestones/<int:milestone_id>/submit', methods=['POST'])
@login_required
def submit_milestone(milestone_id):
    """Freelancer submits a link for milestone completion"""
    milestone = Milestone.query.get_or_404(milestone_id)
    project = milestone.project
    
    # Only assigned freelancer can submit
    if current_user.Role != 'freelancer':
        flash('Only freelancers can submit milestone work!', 'error')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    accepted_bid = Bid.query.filter_by(ProjectID=project.ProjectID, FreelancerID=current_user.UserID, Status='accepted').first()
    if not accepted_bid:
        flash('Access denied!', 'error')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    # Get all milestones ordered by creation (MilestoneID)
    all_milestones = Milestone.query.filter_by(ProjectID=project.ProjectID).order_by(Milestone.MilestoneID).all()
    
    # Check if this milestone can be submitted (sequential order)
    milestone_index = next((i for i, m in enumerate(all_milestones) if m.MilestoneID == milestone_id), None)
    
    if milestone_index is not None:
        # Check if all previous milestones are completed
        if milestone_index > 0:
            previous_milestones = all_milestones[:milestone_index]
            if not all(m.Status == 'completed' for m in previous_milestones):
                flash('⚠️ You must complete previous milestones first! Milestones must be completed in order.', 'warning')
                return redirect(url_for('project_details', project_id=project.ProjectID))
    
    submission_link = request.form.get('submission_link', '').strip()
    if not submission_link:
        flash('Please provide a submission link!', 'error')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    milestone.SubmissionLink = submission_link
    milestone.Status = 'submitted'
    db.session.commit()
    
    flash('✅ Milestone submitted for review!', 'success')
    return redirect(url_for('project_details', project_id=project.ProjectID))

@app.route('/milestones/<int:milestone_id>/complete', methods=['POST'])
@login_required
def complete_milestone(milestone_id):
    """Client marks milestone as complete after reviewing submission"""
    milestone = Milestone.query.get_or_404(milestone_id)
    project = milestone.project
    
    # Only client can mark as complete
    if current_user.UserID != project.ClientID:
        flash('Only the client can mark milestones as complete!', 'error')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    # Check if milestone has been submitted
    if milestone.Status != 'submitted':
        flash('Milestone must be submitted by freelancer before it can be marked complete!', 'warning')
        return redirect(url_for('project_details', project_id=project.ProjectID))
    
    milestone.Status = 'completed'
    
    # Check if all milestones are completed
    all_milestones = Milestone.query.filter_by(ProjectID=project.ProjectID).order_by(Milestone.MilestoneID).all()
    if all_milestones:
        all_completed = all(m.Status == 'completed' for m in all_milestones)
        if all_completed and project.Status == 'in_progress':
            project.Status = 'completed'
            flash('🎉 All milestones completed! Project marked as completed!', 'success')
        else:
            flash('✅ Milestone marked as completed!', 'success')
    else:
        flash('✅ Milestone marked as completed!', 'success')
    
    db.session.commit()
    
    return redirect(url_for('project_details', project_id=project.ProjectID))

# ========================
# PROFILE ROUTES
# ========================

@app.route('/profile')
@login_required
def view_profile():
    user = current_user
    freelancer_profile = None
    reviews_received = []
    
    if user.Role == 'freelancer':
        freelancer_profile = FreelancerProfile.query.filter_by(FreelancerID=user.UserID).first()
        reviews_received = Review.query.filter_by(RevieweeID=user.UserID).all()
    
    return render_template('profile/view_profile.html', 
                         user=user, 
                         freelancer_profile=freelancer_profile,
                         reviews_received=reviews_received)

@app.route('/users/<int:user_id>')
@login_required
def public_profile(user_id):
    user_obj = User.query.get_or_404(user_id)
    freelancer_profile = None
    reviews_received = []
    if user_obj.Role == 'freelancer':
        freelancer_profile = FreelancerProfile.query.filter_by(FreelancerID=user_obj.UserID).first()
        reviews_received = Review.query.filter_by(RevieweeID=user_obj.UserID).all()
    return render_template(
        'profile/public_profile.html',
        user=user_obj,
        freelancer_profile=freelancer_profile,
        reviews_received=reviews_received
    )

@app.route('/profile/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user
    freelancer_profile = None
    
    if user.Role == 'freelancer':
        freelancer_profile = FreelancerProfile.query.filter_by(FreelancerID=user.UserID).first()
    
    if request.method == 'POST':
        user.Name = request.form['name']
        user.Email = request.form['email']
        
        if user.Role == 'freelancer' and freelancer_profile:
            freelancer_profile.Skills = request.form['skills']
            freelancer_profile.Experience = request.form['experience']
            freelancer_profile.PortfolioURL = request.form['portfolio_url']
        
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('view_profile'))
    
    return render_template('profile/edit_profile.html', 
                         user=user, 
                         freelancer_profile=freelancer_profile)

# ========================
# REVIEW ROUTES
# ========================

@app.route('/projects/<int:project_id>/review', methods=['POST'])
@login_required
def submit_review(project_id):
    project = Project.query.get_or_404(project_id)
    
    # Check if project is completed
    if project.Status != 'completed':
        flash('You can only review completed projects!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    rating = request.form['rating']
    comment = request.form['comment']
    reviewee_id = request.form['reviewee_id']
    
    # Validate reviewee is involved in the project
    if int(reviewee_id) not in [project.ClientID] + [bid.FreelancerID for bid in project.bids if bid.Status == 'accepted']:
        flash('Invalid reviewee!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    # Check if review already exists
    existing_review = Review.query.filter_by(
        ProjectID=project_id,
        ReviewerID=current_user.UserID,
        RevieweeID=reviewee_id
    ).first()
    
    if existing_review:
        flash('You have already reviewed this user for this project!', 'error')
        return redirect(url_for('project_details', project_id=project_id))
    
    review = Review(
        ProjectID=project_id,
        ReviewerID=current_user.UserID,
        RevieweeID=reviewee_id,
        Rating=rating,
        Comment=comment
    )
    
    db.session.add(review)
    db.session.commit()
    
    flash('Review submitted successfully!', 'success')
    return redirect(url_for('project_details', project_id=project_id))

# ========================
# ADMIN ROUTES
# ========================

@app.route('/admin/users')
@login_required
def admin_users():
    if current_user.Role != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    users = User.query.all()
    return render_template('admin/users.html', users=users)

@app.route('/admin/projects')
@login_required
def admin_projects():
    if current_user.Role != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    projects = Project.query.all()
    return render_template('admin/projects.html', projects=projects)

@app.route('/admin/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
def admin_edit_user(user_id):
    if current_user.Role != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    if request.method == 'POST':
        user.Name = request.form['name']
        user.Email = request.form['email']
        user.Role = request.form['role']
        
        db.session.commit()
        flash('✅ User updated successfully!', 'success')
        return redirect(url_for('admin_users'))
    
    return render_template('admin/edit_user.html', user=user)

@app.route('/admin/users/<int:user_id>/suspend', methods=['POST'])
@login_required
def admin_suspend_user(user_id):
    if current_user.Role != 'admin':
        flash('Access denied!', 'error')
        return redirect(url_for('index'))
    
    user = User.query.get_or_404(user_id)
    
    # Prevent suspending yourself
    if user.UserID == current_user.UserID:
        flash('⚠️ You cannot suspend yourself!', 'warning')
        return redirect(url_for('admin_users'))
    
    # For now, we'll just show a message (you can add a Suspended field to User model later)
    flash(f'🚫 User {user.Name} has been suspended (feature in development)', 'info')
    return redirect(url_for('admin_users'))

# ========================
# ERROR HANDLERS
# ========================

@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('errors/500.html'), 500

# ========================
# APPLICATION START
# ========================

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)