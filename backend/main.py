from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from scorer import score_startup
from matcher import match_investors
from flag_detector import detect_flags
from memo_generator import generate_memo
from bson import ObjectId

from report_model import (
    save_report,
    reports_collection
)

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

    try:

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

        try:

            save_report(
                data,
                scores,
                flags,
                investors
            )

        except Exception as e:

            print(
                "\nSAVE REPORT ERROR:"
            )
            print(str(e))

        return {

            "scores": scores,
            "investors": investors,
            "flags": flags

        }

    except Exception as e:

        print(
            "\nTEST SCORE ERROR:"
        )
        print(str(e))

        return {
            "error": str(e)
        }


@app.post("/generate-memo")
def generate_memo_route(data: dict):

    try:

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

        try:

            save_report(
                data,
                scores,
                flags,
                investors
            )

        except Exception as e:

            print(
                "\nSAVE REPORT ERROR:"
            )
            print(str(e))

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
        ) as file:

            file.write(
                pdf_bytes
            )

        print(
            "\nPDF GENERATED SUCCESSFULLY"
        )

        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename="startup_memo.pdf"
        )

    except Exception as e:

        print(
            "\nGENERATE MEMO ERROR:"
        )
        print(str(e))

        return {
            "error": str(e)
        }


@app.get("/reports")
def get_reports():
    try:
        reports = []

        for report in reports_collection.find():
            report["_id"] = str(report["_id"])
            reports.append(report)

        return reports

    except Exception as e:
        print("\nREPORT FETCH ERROR:")
        print(str(e))
        return {"error": str(e)}

@app.get("/report/{report_id}")
def get_report(report_id: str):

    report = reports_collection.find_one(
        {
            "_id": ObjectId(report_id)
        }
    )

    if not report:

        return {
            "error": "Report not found"
        }

    report["_id"] = str(
        report["_id"]
    )

    return report   

@app.get("/reports/{startup_name}")
def get_report_by_name(
    startup_name: str
):

    reports = []

    for report in reports_collection.find(
        {
            "startup_data.name": {
                "$regex": startup_name,
                "$options": "i"
            }
        }
    ):

        report["_id"] = str(
            report["_id"]
        )

        reports.append(
            report
        )

    return reports