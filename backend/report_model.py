from pymongo import MongoClient
from datetime import datetime, timezone
import os

client = MongoClient(
    os.getenv(
        "MONGODB_URI",
        "mongodb://localhost:27017"
    )
)

db = client["startuplens"]

reports_collection = db["reports"]


def save_report(
    startup_data,
    scores,
    flags,
    investors,
    competitor_analysis
):

    report = {

        "startup_data":
        startup_data,

        "scores":
        scores,

        "flags":
        flags,

        "investors": investors,
        "competitor_analysis": competitor_analysis,
        "created_at": datetime.now(timezone.utc),
    }

    result = reports_collection.insert_one(
        report
    )

    return str(
        result.inserted_id
    )