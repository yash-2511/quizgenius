import os
import logging
from flask import Flask, render_template, request, jsonify, redirect, url_for
from flask_cors import CORS
from werkzeug.utils import secure_filename
from werkzeug.middleware.proxy_fix import ProxyFix
import json
from datetime import datetime

# Import configuration
from config import config

from file_processor import extract_text_from_file
from gemini_service import generate_quiz_from_text

# Configure logging
log_level = logging.DEBUG if os.environ.get('FLASK_ENV', 'development') == 'development' else logging.INFO
logging.basicConfig(level=log_level)
logger = logging.getLogger(__name__)

def create_app(config_name='default'):
    """Application factory pattern"""
    app = Flask(__name__)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Set up proxy fix for deployment
    app.wsgi_app = ProxyFix(app.wsgi_app, x_proto=1, x_host=1)
    
    # Enable CORS
    CORS(app)
    
    return app

# Create app instance
config_name = os.environ.get('FLASK_ENV', 'development')
app = create_app(config_name)

# In-memory storage for MVP
quiz_storage = {}
file_storage = {}

def allowed_file(filename):
    """Check if file extension is allowed"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    """Render the main page"""
    return render_template('index.html')

@app.route('/health')
def health_check():
    """Health check endpoint for monitoring"""
    return jsonify({
        'status': 'healthy',
        'service': 'AI Quiz Generator',
        'version': '1.0.0'
    })

@app.route('/upload', methods=['POST'])
def upload_file():
    """Handle file upload and generate quiz"""
    try:
        # Check if file is present
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        
        # Check if file is selected
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        # Check if file type is allowed
        if not allowed_file(file.filename):
            return jsonify({'error': 'File type not supported. Please upload PDF or DOCX files.'}), 400
        
        # Save file
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(str(app.config['UPLOAD_FOLDER']), unique_filename)
        file.save(file_path)
        
        logger.info(f"File saved: {file_path}")
        
        # Extract text from file
        try:
            extracted_text = extract_text_from_file(file_path)
            if not extracted_text or len(extracted_text.strip()) < 50:
                return jsonify({'error': 'Could not extract sufficient text from the file. Please ensure the file contains readable text.'}), 400
            
            logger.info(f"Extracted text length: {len(extracted_text)}")
            
        except Exception as e:
            logger.error(f"Text extraction error: {str(e)}")
            return jsonify({'error': f'Failed to extract text from file: {str(e)}'}), 500
        
        # Generate quiz using Gemini API
        try:
            quiz_data = generate_quiz_from_text(extracted_text)
            
            # Generate unique quiz ID
            quiz_id = f"quiz_{timestamp}_{len(quiz_storage)}"
            
            # Store quiz and file info
            quiz_storage[quiz_id] = {
                'quiz': quiz_data,
                'filename': filename,
                'created_at': datetime.now().isoformat(),
                'text_length': len(extracted_text)
            }
            
            file_storage[quiz_id] = {
                'original_filename': filename,
                'file_path': file_path,
                'text': extracted_text[:500] + "..." if len(extracted_text) > 500 else extracted_text
            }
            
            logger.info(f"Quiz generated successfully with ID: {quiz_id}")
            
            return jsonify({
                'success': True,
                'quiz_id': quiz_id,
                'message': 'Quiz generated successfully!',
                'filename': filename
            })
            
        except Exception as e:
            logger.error(f"Quiz generation error: {str(e)}")
            return jsonify({'error': f'Failed to generate quiz: {str(e)}'}), 500
        
        finally:
            # Clean up uploaded file
            try:
                if os.path.exists(file_path):
                    os.remove(file_path)
                    logger.info(f"Cleaned up file: {file_path}")
            except Exception as e:
                logger.warning(f"Could not clean up file {file_path}: {str(e)}")
    
    except Exception as e:
        logger.error(f"Upload error: {str(e)}")
        return jsonify({'error': f'Upload failed: {str(e)}'}), 500

@app.route('/quiz/<quiz_id>')
def get_quiz(quiz_id):
    """Get quiz data by ID"""
    try:
        if quiz_id not in quiz_storage:
            return jsonify({'error': 'Quiz not found'}), 404
        
        quiz_data = quiz_storage[quiz_id]
        file_info = file_storage.get(quiz_id, {})
        
        return jsonify({
            'success': True,
            'quiz': quiz_data['quiz'],
            'filename': quiz_data['filename'],
            'created_at': quiz_data['created_at'],
            'text_preview': file_info.get('text', '')
        })
    
    except Exception as e:
        logger.error(f"Error retrieving quiz {quiz_id}: {str(e)}")
        return jsonify({'error': f'Failed to retrieve quiz: {str(e)}'}), 500

@app.route('/quizzes')
def list_quizzes():
    """List all available quizzes"""
    try:
        quizzes = []
        for quiz_id, data in quiz_storage.items():
            quizzes.append({
                'quiz_id': quiz_id,
                'filename': data['filename'],
                'created_at': data['created_at'],
                'question_count': len(data['quiz'].get('questions', []))
            })
        
        # Sort by creation time, newest first
        quizzes.sort(key=lambda x: x['created_at'], reverse=True)
        
        return jsonify({
            'success': True,
            'quizzes': quizzes
        })
    
    except Exception as e:
        logger.error(f"Error listing quizzes: {str(e)}")
        return jsonify({'error': f'Failed to list quizzes: {str(e)}'}), 500

@app.errorhandler(413)
def too_large(e):
    """Handle file too large error"""
    return jsonify({'error': 'File too large. Maximum size is 16MB.'}), 413

@app.errorhandler(500)
def internal_error(e):
    """Handle internal server errors"""
    logger.error(f"Internal server error: {str(e)}")
    return jsonify({'error': 'Internal server error occurred.'}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
