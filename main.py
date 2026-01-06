from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"service": "microservice-3", "status": "ok"}
