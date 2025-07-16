
import json
import logging
import os
from typing import Dict, List, Any
from google import genai
from google.genai import types
from pydantic import BaseModel

logger = logging.getLogger(__name__)

# Initialize Gemini client with secure API key from environment
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise ValueError("GEMINI_API_KEY not set in environment. Please check your .env or Render settings.")

client = genai.Client(api_key=api_key)

# Pydantic schemas
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
    """
    try:
        max_chars = 8000
        if len(text) > max_chars:
            text = text[:max_chars] + "..."
            logger.info(f"Text truncated to {max_chars} characters for Gemini input")

        # Very strict prompt to enforce proper JSON
        system_prompt = (
            "You are an expert quiz generator. "
            "ONLY return valid JSON as specified. No extra comments or explanations outside JSON. "
            "Ensure all strings are enclosed in double quotes and JSON is well-formed."
        )

        user_prompt = f"""
Generate exactly 5 multiple choice questions from this text:

{text}

Return only valid JSON with this exact structure, nothing else:
{{
    "questions": [
        {{
            "question": "Question text here?",
            "options": ["Option A", "Option B", "Option C", "Option D"],
            "correct_answer": 0,
            "explanation": "Short explanation"
        }}
    ],
    "total_questions": 5
}}

IMPORTANT:
- Do NOT include any text outside this JSON.
- Do NOT use markdown or comments.
- Ensure all arrays and strings are closed properly.
- This JSON will be parsed directly by json.loads(). Invalid JSON will break the system.
"""

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

        logger.info("Received response from Gemini API")

        if not response.text:
            raise ValueError("Empty response from Gemini API")

        # Attempt to parse the JSON
        try:
            quiz_data = json.loads(response.text)
        except json.JSONDecodeError as e:
            logger.error(f"JSON parsing error: {str(e)}")
            # Log raw Gemini response for debug
            with open("gemini_raw_response_error.log", "w") as f:
                f.write(response.text)
            raise Exception(f"Failed to parse quiz response JSON: {str(e)}")

        # Validate structure
        if 'questions' not in quiz_data or not isinstance(quiz_data['questions'], list):
            raise ValueError("Invalid quiz format: missing or malformed 'questions'")

        # Validate individual questions
        for i, question in enumerate(quiz_data['questions']):
            for field in ['question', 'options', 'correct_answer', 'explanation']:
                if field not in question:
                    raise ValueError(f"Question {i+1} missing field '{field}'")
            if len(question['options']) != 4:
                raise ValueError(f"Question {i+1} must have exactly 4 options")
            if question['correct_answer'] not in [0,1,2,3]:
                raise ValueError(f"Question {i+1} correct_answer must be 0,1,2,3")

        logger.info(f"Successfully generated {len(quiz_data['questions'])} questions")

        return quiz_data

    except Exception as e:
        logger.error(f"Quiz generation error: {str(e)}")
        raise Exception(f"Failed to generate quiz: {str(e)}")

