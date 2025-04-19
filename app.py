from flask import Flask, render_template, request, redirect, url_for # type: ignore
from flask_wtf.csrf import CSRFProtect # type: ignore
from werkzeug.utils import secure_filename # type: ignore
from analyzer import ResumeParser, ResumeRanker, FeedbackGenerator
import os
import json

app = Flask(__name__)
app.secret_key = 'your-secret-key-123'  # Replace with a real secret key
app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024  # 5MB limit

# Initialize CSRF protection
csrf = CSRFProtect(app)

# Ensure upload directory exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def load_role_benchmarks():
    """Load role requirements from JSON file"""
    try:
        with open('analyzer/role_benchmarks.json') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        app.logger.error(f"Error loading benchmarks: {str(e)}")
        return {}

@app.route('/')
def index():
    """Render the main upload form"""
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    """Process uploaded resume"""
    if 'resume' not in request.files:
        return redirect(url_for('index'))
    
    file = request.files['resume']
    if file.filename == '':
        return redirect(url_for('index'))
    
    if file and allowed_file(file.filename):
        try:
            # Secure filename handling
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Get selected role
            role = request.form.get('role', '').strip().lower()
            if not role:
                raise ValueError("No role selected")
            
            # Load benchmarks
            benchmarks = load_role_benchmarks().get(role, {})
            required_skills = benchmarks.get("required_skills", [])
            exp_levels = benchmarks.get("experience_levels", {})
            
            # Initialize components
            parser = ResumeParser()
            ranker = ResumeRanker()
            feedback_gen = FeedbackGenerator()
            
            # Process resume
            resume_data = parser.parse(filepath)
            
            # Calculate ranking
            ranking = ranker.rank(
                resume_data=resume_data,
                required_skills=required_skills,
                exp_levels=exp_levels
            )
            
            # Generate feedback
            feedback = feedback_gen.generate(
                resume_data=resume_data,
                ranking=ranking,
                role=role
            )
            
            return render_template(
                'results.html',
                role=role.replace('_', ' ').title(),
                score=round(ranking['score'], 2),
                strengths=feedback.get('strengths', []),
                improvements=feedback.get('improvements', [])
            )
            
        except Exception as e:
            app.logger.error(f"Error processing resume: {str(e)}")
            return render_template('error.html', error_message=str(e))
            
        finally:
            if os.path.exists(filepath):
                os.remove(filepath)
    
    return redirect(url_for('index'))

def allowed_file(filename):
    """Check allowed file extensions"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in {'pdf', 'docx'}

if __name__ == '__main__':
    app.run(debug=True, port=5001)  # Changed port to avoid conflicts