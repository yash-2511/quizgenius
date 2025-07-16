# AI Quiz Generator from Notes

An AI-powered web application that extracts text from uploaded documents (PDF, DOCX) and generates interactive multiple-choice quizzes using Google Gemini AI.

## Features

- **Document Upload**: Support for PDF and DOCX file formats
- **AI-Powered Quiz Generation**: Uses Google Gemini API to create meaningful MCQ questions
- **Interactive Quiz Interface**: Clean, responsive design with real-time feedback
- **Answer Validation**: Immediate results with explanations for correct answers
- **Quiz History**: View and retake previously generated quizzes
- **File Processing**: Robust text extraction from various document formats

## Tech Stack

### Backend
- **Flask**: Web framework
- **Flask-CORS**: Cross-origin resource sharing
- **PyMuPDF**: PDF text extraction
- **python-docx**: DOCX text extraction
- **google-genai**: Google Gemini AI integration
- **Werkzeug**: File handling utilities

### Frontend
- **HTML5**: Modern markup
- **Bootstrap 5**: Responsive UI framework with dark theme
- **Vanilla JavaScript**: Client-side functionality
- **Font Awesome**: Icons

## Setup Instructions

### Prerequisites

1. **Python 3.8+** installed on your system
2. **Google Gemini API Key** (get it from [Google AI Studio](https://makersuite.google.com/app/apikey))

### Installation

#### Option 1: Quick Setup (Recommended)

1. **Download and run the setup script**:
   ```bash
   python local_setup.py --install-deps
   ```

2. **Edit the .env file** and add your Gemini API key:
   ```bash
   GEMINI_API_KEY=your_actual_api_key_here
   ```

3. **Start the application**:
   ```bash
   python run_local.py
   ```

#### Option 2: Manual Setup

1. **Clone or create the project directory**:
   ```bash
   mkdir ai-quiz-generator
   cd ai-quiz-generator
   ```

2. **Install required packages**:
   ```bash
   pip install flask flask-cors google-genai pymupdf python-docx pydantic werkzeug
   ```

3. **Create environment file**:
   ```bash
   cp .env.example .env
   # Edit .env and add your GEMINI_API_KEY
   ```

4. **Run the application**:
   ```bash
   python run_local.py
   ```

## Local Development Files

The project includes several configuration files for easy local setup:

- **`config.py`** - Configuration management for different environments
- **`run_local.py`** - Local development server with environment setup
- **`local_setup.py`** - Automated setup script for dependencies and directories
- **`.env.example`** - Template for environment variables

## Usage

1. **Start the server**:
   ```bash
   python run_local.py
   ```

2. **Open your browser** and go to `http://localhost:5000`

3. **Upload a document**:
   - Click "Choose File" or drag and drop a PDF/DOCX file
   - Supported formats: PDF, DOCX (max 16MB)

4. **Take the quiz**:
   - Answer the generated multiple-choice questions
   - Submit to see results with explanations

5. **View quiz history**:
   - Previous quizzes are saved and can be retaken

## Project Structure

```
ai-quiz-generator/
├── app.py                 # Main Flask application
├── main.py               # Entry point for deployment
├── config.py             # Configuration management
├── run_local.py          # Local development server
├── local_setup.py        # Setup automation script
├── file_processor.py     # Document text extraction
├── gemini_service.py     # AI quiz generation
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── style.css         # Custom styling
│   └── script.js         # Frontend JavaScript
├── uploads/              # Temporary file storage
├── .env.example          # Environment template
└── README.md             # This file
```

## API Endpoints

- **`GET /`** - Main application page
- **`POST /upload`** - Upload document and generate quiz
- **`GET /quiz/<quiz_id>`** - Retrieve specific quiz
- **`GET /quizzes`** - List all generated quizzes

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `GEMINI_API_KEY` | Google Gemini API key | Yes |
| `SESSION_SECRET` | Flask session secret | No (has default) |
| `FLASK_ENV` | Environment (development/production) | No (defaults to development) |
| `FLASK_DEBUG` | Debug mode | No (defaults to True) |

## Features in Detail

### Document Processing
- **PDF Support**: Extracts text from all pages using PyMuPDF
- **DOCX Support**: Extracts text from paragraphs and tables using python-docx
- **Error Handling**: Graceful fallbacks and detailed error messages

### AI Quiz Generation
- **Gemini Integration**: Uses Google's latest Gemini 2.5 Flash model
- **Structured Output**: Pydantic models ensure consistent quiz format
- **Quality Questions**: AI generates meaningful MCQs with explanations

### User Interface
- **Responsive Design**: Works on desktop and mobile devices
- **Dark Theme**: Modern dark UI using Bootstrap
- **Real-time Feedback**: Progress indicators and immediate results
- **Drag & Drop**: Easy file upload with visual feedback

## Troubleshooting

### Common Issues

1. **"GEMINI_API_KEY not found"**:
   - Ensure you've added your API key to the .env file
   - Check the key starts with "AIza"

2. **"File type not supported"**:
   - Only PDF and DOCX files are supported
   - Check file isn't corrupted

3. **"Failed to extract text"**:
   - Ensure the document contains readable text
   - Some PDFs with images-only won't work

4. **Import errors**:
   - Run: `pip install flask flask-cors google-genai pymupdf python-docx pydantic`

### Getting API Key

1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account  
3. Click "Create API Key"
4. Copy the key (starts with "AIza...")
5. Add it to your .env file

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.
   