
from fastapi import FastAPI
from aurabackend.shared.models import ExecutionJob, QueryResult

execution_app = FastAPI()

@execution_app.post("/execute_sql")
async def execute_sql(job: ExecutionJob):
	# TODO: Connect to DB, run SQL, return result
	return QueryResult(columns=["product_name", "total_revenue"], rows=[["Widget", 1000], ["Gadget", 2000]], chart_spec={"type": "bar"})
