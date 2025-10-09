
from fastapi import FastAPI, Request
from aurabackend.shared.models import PlanStep

code_gen_app = FastAPI()

@code_gen_app.post("/generate_code")
async def generate_code(step: PlanStep):
	# TODO: Integrate with Gemini or other LLM
	return {"sql": "SELECT * FROM sales_table;", "visualization_suggestion": "bar_chart"}
