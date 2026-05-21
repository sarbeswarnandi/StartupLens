from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from scorer import score_startup

app = FastAPI(
    title="StartupLens API",
    version="1.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "message": "StartupLens API running"
    }


@app.get("/health")
def health():
    return {
        "status": "ok"
    }


@app.post("/test-score")
def test_score(data: dict = Body(...)):

    result = score_startup(data)

    return result