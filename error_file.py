"""
This module contains all the error responses to be sent
"""

errors = {
    "SUCCESS": {"respcode": 200, "respdesc": "Success"},
    "EMPTY_REQUEST_BODY": {"respcode": 400, "respdesc": "Bad request"},
    "INVALID_HEADERS": {"respcode": 401, "respdesc": "Invalid headers"},
    "INVALID_VOTER_NUMBER": {"respcode": 402, "respdesc": "Invalid voter_id"},
    "INVALID_REQUEST": {"respcode": 403, "respdesc": "Invalid request"},
    "INTERNAL_ERROR": {"respcode": 500, "respdesc": "Internal error occurred"},
    "DETAILS_FETCHING_FAILED": {
        "respcode": 501,
        "respdesc": "Details fetaching failed"
        },
    "DETAILS_NOT_FOUND": {"respcode": 502, "respdesc": "No record found for this ID"},
    "SERVER_BUSY": {"respcode": 503, "respdesc": "Server busy"},
    "CONNECTION_ERROR": {"respcode": 504, "respdesc": "Connection error"}
}
