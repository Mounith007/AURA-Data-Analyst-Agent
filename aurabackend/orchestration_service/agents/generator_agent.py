
import os
import google.generativeai as genai

from aurabackend.shared.models import ValidationResult

class GeneratorAgent:
    """
    Generates an SQL query based on the user's prompt and database context.
    It can incorporate feedback from the Critic Agent for rework attempts.
    """
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-pro')

    def run(self, prompt: str, context: str, rework_feedback: str = "") -> str:
        """
        Constructs a prompt and calls the Gemini API to generate SQL.
        """
        instruction = (
            "You are an expert data analyst. Your task is to convert a user's question "
            "into a syntactically correct SQL query for a PostgreSQL database. "
            "Use the provided database schema context. Respond ONLY with the SQL query."
        )

        prompt_parts = [
            instruction,
            f"Database Schema Context:\n{context}",
            f"User's question:\n{prompt}"
        ]

        if rework_feedback:
            prompt_parts.append(
                "This is a rework attempt. The previous query was flawed. "
                f"Please correct it based on this feedback:\n{rework_feedback}"
            )
        
        try:
            response = self.model.generate_content(prompt_parts)
            # Clean up the response to ensure it's just the SQL query
            generated_sql = response.text.strip().replace("```sql", "").replace("```", "").strip()
            return generated_sql
        except Exception as e:
            print(f"Error during generation: {e}")
            return f"-- ERROR: Could not generate SQL query. Details: {e}"