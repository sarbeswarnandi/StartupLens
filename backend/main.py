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

@app.get("/analytics")
def get_analytics():

    reports = list(
        reports_collection.find()
    )

    total_reports = len(
        reports
    )

    if total_reports == 0:

        return {
            "total_reports": 0,
            "average_fundability": 0,
            "top_sector": "N/A",
            "highest_startup": "N/A"
        }

    fundability_scores = []

    sector_count = {}

    highest_score = 0

    highest_startup = "N/A"

    for report in reports:

        score = report.get(
            "scores",
            {}
        ).get(
            "fundability_score",
            0
        )

        fundability_scores.append(
            score
        )

        if score > highest_score:

            highest_score = score

            highest_startup = (
                report
                .get(
                    "startup_data",
                    {}
                )
                .get(
                    "name",
                    "Unknown"
                )
            )

        sector = (
            report
            .get(
                "startup_data",
                {}
            )
            .get(
                "sector",
                "Unknown"
            )
        )

        sector_count[
            sector
        ] = (
            sector_count.get(
                sector,
                0
            ) + 1
        )

    top_sector = max(
        sector_count,
        key=sector_count.get
    )

    return {

        "total_reports":
        total_reports,

        "average_fundability":
        round(
            sum(
                fundability_scores
            ) /
            total_reports,
            2
        ),

        "top_sector":
        top_sector,

        "highest_startup":
        highest_startup,

        "highest_score":
        highest_score
    }

@app.get("/analytics")
def get_analytics():

    try:

        reports = list(
            reports_collection.find()
        )

        total_reports = len(
            reports
        )

        if total_reports == 0:

            return {

                "total_reports": 0,

                "average_fundability": 0,

                "top_sector": "N/A",

                "highest_startup": "N/A",

                "highest_score": 0
            }

        fundability_scores = []

        sector_count = {}

        highest_score = 0

        highest_startup = "N/A"

        for report in reports:

            score = (
                report
                .get("scores", {})
                .get(
                    "fundability_score",
                    0
                )
            )

            fundability_scores.append(
                score
            )

            if score > highest_score:

                highest_score = score

                highest_startup = (
                    report
                    .get(
                        "startup_data",
                        {}
                    )
                    .get(
                        "name",
                        "Unknown"
                    )
                )

            sector = (
                report
                .get(
                    "startup_data",
                    {}
                )
                .get(
                    "sector",
                    "Unknown"
                )
            )

            sector_count[sector] = (
                sector_count.get(
                    sector,
                    0
                ) + 1
            )

        top_sector = max(
            sector_count,
            key=sector_count.get
        )

        return {

            "total_reports":
            total_reports,

            "average_fundability":
            round(
                sum(
                    fundability_scores
                ) /
                total_reports,
                2
            ),

            "top_sector":
            top_sector,

            "highest_startup":
            highest_startup,

            "highest_score":
            highest_score
        }

    except Exception as e:

        return {
            "error": str(e)
        }
    
@app.delete("/report/{report_id}")
def delete_report(
    report_id: str
):

    result = reports_collection.delete_one(
        {
            "_id": ObjectId(
                report_id
            )
        }
    )

    if result.deleted_count == 0:

        return {
            "error":
            "Report not found"
        }

    return {
        "message":
        "Report deleted successfully"
    }