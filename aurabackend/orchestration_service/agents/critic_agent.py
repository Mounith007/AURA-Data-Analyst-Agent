import os
import json
import google.generativeai as genai
from aurabackend.shared.models import ValidationResult

# Configure the Gemini API key from .env file
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class CriticAgent:
    """
    Validates a generated SQL query for correctness, security, and alignment
    with the user's original intent.
    """
    def __init__(self):
        # Using a model that is good at following JSON instructions
        self.model = genai.GenerativeModel(
            'gemini-pro',
            generation_config=genai.GenerationConfig(response_mime_type="application/json")
        )

    def run(self, original_prompt: str, generated_sql: str) -> ValidationResult:
        """
        Constructs a validation prompt and calls the Gemini API.
        """
        instruction = (
            "You are a senior data architect acting as a meticulous code reviewer. "
            "Analyze the provided SQL query based on the user's original request. "
            "Check for: 1. Syntactic correctness. 2. Security vulnerabilities. "
            "3. Correctness in addressing the user's request. "
            "Respond ONLY with a JSON object matching the specified format."
        )

        prompt = f"""
        {instruction}

        "user_request": "{original_prompt}",
        "sql_query": "{generated_sql}",

        "response_format": {{
            "is_valid": "boolean",
            "reason": "string",
            "rework_suggestion": "string (provide if invalid)"
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            response_json = json.loads(response.text)
            return ValidationResult(**response_json)
        except Exception as e:
            print(f"Error during validation: {e}")
            return ValidationResult(
                is_valid=False,
                reason=f"An exception occurred during validation: {e}",
                rework_suggestion="The validation agent failed. Please check the system logs."
            )