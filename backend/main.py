from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from scorer import score_startup
from matcher import match_investors
from flag_detector import detect_flags
from memo_generator import generate_memo
from fastapi.responses import FileResponse
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
def test_score(data: dict):

    scores = score_startup(
        data
    )

    investors = match_investors(
        data,
        scores
    )

    flags = detect_flags(
        data,
        scores
    )

    return {

        "scores":
        scores,

        "investors":
        investors,

        "flags":
        flags
    }
@app.post("/generate-memo")
def generate_memo_route(data: dict):

    scores = score_startup(
        data
    )

    investors = match_investors(
        data,
        scores
    )

    flags = detect_flags(
        data,
        scores
    )

    pdf_bytes = generate_memo(
        data,
        scores,
        flags,
        investors
    )

    file_path = "startup_memo.pdf"

    with open(
        file_path,
        "wb"
    ) as f:

        f.write(pdf_bytes)

    return FileResponse(
        path=file_path,
        media_type="application/pdf",
        filename="startup_memo.pdf"
    )