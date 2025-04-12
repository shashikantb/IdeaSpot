from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'  # Fixed typo in DATABASE_URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Models
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), nullable=False, default='viewer')  # 'poster' or 'viewer'
    ideas = db.relationship('Idea', backref='author', lazy=True)

class Idea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

# Routes
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        role = request.form.get('role')
        
        # Fixed password hashing method
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
        
        user = User(username=username, email=email, password=hashed_password, role=role)
        db.session.add(user)
        db.session.commit()
        
        flash('Account created successfully! You can now login.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Login unsuccessful. Please check username and password.', 'danger')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('home'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))
    
    return render_template('dashboard.html', role=session.get('role'))

@app.route('/post_idea', methods=['GET', 'POST'])
def post_idea():
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))
    
    if session.get('role') != 'poster':
        flash('Only posters can submit business ideas.', 'danger')
        return redirect(url_for('dashboard'))
    
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        
        idea = Idea(title=title, content=content, user_id=session['user_id'])
        db.session.add(idea)
        db.session.commit()
        
        flash('Your idea has been posted!', 'success')
        return redirect(url_for('view_ideas'))
    
    return render_template('post_idea.html')

@app.route('/view_ideas')
def view_ideas():
    if 'user_id' not in session:
        flash('Please login to access this page.', 'warning')
        return redirect(url_for('login'))
    
    ideas = Idea.query.order_by(Idea.date_posted.desc()).all()
    return render_template('view_ideas.html', ideas=ideas)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    port = int(os.environ.get("PORT", 3000))
    app.run(host='0.0.0.0', port=port)