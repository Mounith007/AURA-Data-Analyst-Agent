
from fastapi import FastAPI

metadata_app = FastAPI()

@metadata_app.get("/get_user")
async def get_user(user_id: str):
	# TODO: Integrate with PostgreSQL or other DB
	return {"user_id": user_id, "name": "Test User"}
