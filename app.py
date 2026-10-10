import os
import sqlite3
import uuid
import re
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, g, abort
from flask_wtf.csrf import CSRFProtect, CSRFError
from dotenv import load_dotenv

# Load environment variables from .env if present
load_dotenv()

app = Flask(__name__)
# Configuration for security and database
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-prod')
app.config['DATABASE'] = os.path.join(app.root_path, 'database', 'applynow.db')

# Enable CSRF Protection
csrf = CSRFProtect(app)

# Allowed predefined options for validation
ALLOWED_POSITIONS = [
    "Python Developer", "Data Analyst", "Frontend Developer", 
    "Backend Developer", "Data Scientist", "UI/UX Designer", 
    "Digital Marketing Executive", "Business Development Associate"
]
ALLOWED_EXPERIENCE = [
    "Entry Level / Fresher", "1–2 Years", "3–5 Years", "5+ Years"
]

# --- Database Management ---
def get_db():
    """Get the active SQLite database connection for this request."""
    db = getattr(g, '_database', None)
    if db is None:
        # Ensure the database directory exists
        db_dir = os.path.dirname(app.config['DATABASE'])
        if not os.path.exists(db_dir):
            os.makedirs(db_dir)
            
        db = g._database = sqlite3.connect(app.config['DATABASE'])
        db.row_factory = sqlite3.Row  # Return dictionary-like rows
    return db

@app.teardown_appcontext
def close_connection(exception):
    """Close the database connection cleanly at the end of the request."""
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db():
    """Initialize the SQLite schema automatically."""
    with app.app_context():
        db = get_db()
        db.execute('''
            CREATE TABLE IF NOT EXISTS applications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                reference TEXT UNIQUE NOT NULL,
                full_name TEXT NOT NULL,
                email TEXT NOT NULL,
                position TEXT NOT NULL,
                experience_level TEXT NOT NULL,
                cover_letter TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL
            )
        ''')
        db.commit()

# Initialize DB when the app starts
init_db()

# --- Helpers ---
def is_valid_email(email):
    """Basic server-side email validation regex."""
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email) is not None

# --- Routes ---

@app.route('/', methods=['GET'])
def index():
    """
    Render the home page and job application form.
    This demonstrates a GET request.
    """
    return render_template('index.html', 
                           positions=ALLOWED_POSITIONS, 
                           experience_levels=ALLOWED_EXPERIENCE)

@app.route('/apply', methods=['POST'])
def apply():
    """
    Handle the job application submission.
    This demonstrates a POST request and the Post/Redirect/Get pattern.
    """
    # 1. Retrieve and trim form fields
    full_name = request.form.get('full_name', '').strip()
    email = request.form.get('email', '').strip()
    position = request.form.get('position', '').strip()
    experience = request.form.get('experience_level', '').strip()
    cover_letter = request.form.get('cover_letter', '').strip()
    consent = request.form.get('consent')
    
    errors = {}
    
    # 2. Server-side Validations
    if not full_name or len(full_name) < 2:
        errors['full_name'] = "Full name must be at least 2 characters."
        
    if not email or not is_valid_email(email):
        errors['email'] = "Please provide a valid email address."
        
    if position not in ALLOWED_POSITIONS:
        errors['position'] = "Please select a valid position."
        
    if experience not in ALLOWED_EXPERIENCE:
        errors['experience'] = "Please select a valid experience level."
        
    if not cover_letter or len(cover_letter) < 30 or len(cover_letter) > 2000:
        errors['cover_letter'] = "Cover letter must be between 30 and 2000 characters."
        
    if not consent:
        errors['consent'] = "You must confirm the accuracy of your information."

    # If validation fails, re-render form with errors and previous input
    if errors:
        return render_template('index.html', 
                               positions=ALLOWED_POSITIONS, 
                               experience_levels=ALLOWED_EXPERIENCE,
                               errors=errors,
                               form_data=request.form), 400
                               
    # 3. Validation succeeded: Save to SQLite using parameterized queries
    reference = f"AN-{uuid.uuid4().hex[:8].upper()}"
    
    try:
        db = get_db()
        db.execute('''
            INSERT INTO applications (reference, full_name, email, position, experience_level, cover_letter, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (reference, full_name, email, position, experience, cover_letter, datetime.now().isoformat()))
        db.commit()
    except sqlite3.Error as e:
        app.logger.error(f"Database error during insert: {e}")
        abort(500)
        
    # 4. Post/Redirect/Get Pattern: Redirect to a GET confirmation route
    # This prevents duplicate form submissions on browser refresh.
    return redirect(url_for('application_success', reference=reference))

@app.route('/application-success/<reference>', methods=['GET'])
def application_success(reference):
    """
    Display a dedicated application confirmation page.
    Retrieves data based on the unique application reference.
    """
    db = get_db()
    cursor = db.execute('SELECT * FROM applications WHERE reference = ?', (reference,))
    application = cursor.fetchone()
    
    # If the reference doesn't exist, return a 404 error
    if application is None:
        abort(404)
        
    return render_template('success.html', app=application)

@app.route('/admin/submissions', methods=['GET'])
def admin_submissions():
    """Hidden route to view all submissions for demonstration purposes."""
    db = get_db()
    cursor = db.execute('SELECT * FROM applications ORDER BY created_at DESC')
    applications = cursor.fetchall()
    return render_template('submissions.html', applications=applications)

@app.route('/about', methods=['GET'])
def about():
    """Simple About page describing ApplyNow."""
    return render_template('about.html')

# --- Error Handlers ---
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500
    
@app.errorhandler(CSRFError)
def handle_csrf_error(e):
    # Handle missing or invalid CSRF tokens gracefully
    return render_template('404.html', custom_message="Your session expired or the form submission was invalid. Please try again."), 400

if __name__ == '__main__':
    # Run the application in debug mode for local development
    app.run(debug=True)
