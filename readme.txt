business-idea-app/
├── app.py
├── requirements.txt
├── static/
│   └── style.css
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── post_idea.html
│   └── view_ideas.html
└── instance/
    └── site.db (will be created when you first run the app)
	
==================
Structure for app.py

# Basic routes first
@app.route('/')
def home()

@app.route('/login')
def login()

@app.route('/register')
def register()

# Authenticated routes next
@app.route('/dashboard')
def dashboard()

@app.route('/account')  # This must come before any templates use url_for('account')
def account()

# Other routes...	
	
	
	
	
	
	
	
	
	
	
	