
from fastapi import FastAPI

kb_app = FastAPI()

@kb_app.get("/get_schema")
async def get_schema(table: str):
	# TODO: Integrate with vector DB and metadata store
	return {"schema": f"Schema for {table}: product_name, total_revenue, sale_date"}
