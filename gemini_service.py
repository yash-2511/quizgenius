import json
import logging
import os
from typing import Dict, List, Any

from google import genai
from google.genai import types
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Initialize Gemini client
client = genai.Client(api_key=os.environ.get("GEMINI_API_KEY", "default_key"))

class QuizQuestion(BaseModel):
    question: str
    options: List[str]
    correct_answer: int
    explanation: str

class QuizResponse(BaseModel):
    questions: List[QuizQuestion]
    total_questions: int

def generate_quiz_from_text(text: str) -> Dict[str, Any]:
    """
    Generate a quiz from extracted text using Gemini API
    
    Args:
        text (str): The extracted text from the document
        
    Returns:
        Dict[str, Any]: Generated quiz data
        
    Raises:
        Exception: If quiz generation fails
    """
    try:
        # Truncate text if too long (Gemini has token limits)
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            logger.info(f"Text truncated to {max_chars} characters")
        
        # Create the prompt for quiz generation
        system_prompt = (
            "You are an expert quiz generator. Generate exactly 5 multiple choice questions from the provided text. "
            "Each question should test understanding of key concepts from the text. "
            "For each question, provide exactly 4 options and indicate which option is correct (0-3). "
            "Also provide a brief explanation for the correct answer. "
            "Make sure questions are clear, options are plausible, and there's only one correct answer per question."
        )
        
        user_prompt = f"""Generate 5 multiple choice questions from this text:

{text}

Format your response as JSON with this exact structure:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Brief explanation of why this is correct"
        }}
    ],
    "total_questions": 5
}}

Ensure all questions are based on the content provided and test comprehension of the material."""

        logger.info("Sending request to Gemini API for quiz generation")
        
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=[
                types.Content(role="user", parts=[types.Part(text=user_prompt)])
            ],
            config=types.GenerateContentConfig(
                system_instruction=system_prompt,
                response_mime_type="application/json",
                response_schema=QuizResponse,
                temperature=0.7,
                max_output_tokens=2048
            ),
        )
        
        if not response.text:
            raise ValueError("Empty response from Gemini API")
        
        logger.info("Received response from Gemini API")
        logger.debug(f"Raw response: {response.text}")
        
        # Parse the JSON response
        quiz_data = json.loads(response.text)
        
        # Validate the response structure
        if 'questions' not in quiz_data:
            raise ValueError("Invalid response format: missing 'questions' field")
        
        questions = quiz_data['questions']
        if not questions or len(questions) == 0:
            raise ValueError("No questions generated")
        
        # Validate each question
        for i, question in enumerate(questions):
            required_fields = ['question', 'options', 'correct_answer', 'explanation']
            for field in required_fields:
                if field not in question:
                    raise ValueError(f"Question {i+1} missing required field: {field}")
            
            if not isinstance(question['options'], list) or len(question['options']) != 4:
                raise ValueError(f"Question {i+1} must have exactly 4 options")
            
            if not isinstance(question['correct_answer'], int) or question['correct_answer'] not in [0, 1, 2, 3]:
                raise ValueError(f"Question {i+1} correct_answer must be 0, 1, 2, or 3")
        
        logger.info(f"Successfully generated {len(questions)} questions")
        
        return quiz_data
        
    except json.JSONDecodeError as e:
        logger.error(f"JSON parsing error: {str(e)}")
        raise Exception(f"Failed to parse quiz response: {str(e)}")
    
    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}")
        raise Exception(f"Failed to generate quiz: {str(e)}")

def validate_quiz_data(quiz_data: Dict[str, Any]) -> bool:
    """
    Validate quiz data structure
    
    Args:
        quiz_data (Dict[str, Any]): Quiz data to validate
        
    Returns:
        bool: True if valid, False otherwise
    """
    try:
        if not isinstance(quiz_data, dict):
            return False
        
        if 'questions' not in quiz_data:
            return False
        
        questions = quiz_data['questions']
        if not isinstance(questions, list) or len(questions) == 0:
            return False
        
        for question in questions:
            if not isinstance(question, dict):
                return False
            
            required_fields = ['question', 'options', 'correct_answer', 'explanation']
            if not all(field in question for field in required_fields):
                return False
            
            if not isinstance(question['options'], list) or len(question['options']) != 4:
                return False
            
            if not isinstance(question['correct_answer'], int) or question['correct_answer'] not in [0, 1, 2, 3]:
                return False
        
        return True
        
    except Exception:
        return False
