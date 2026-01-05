from fastapi import FastAPI
from neuroos_app.api.tasks import router as task_router

app = FastAPI()

@app.get("/")
def root():
    return {"status": "NeuroOS backend is running"}

app.include_router(task_router)