import requests
import json
import os
from logging_helper import get_logger
from dotenv import load_dotenv
from error_file import errors
from utils_1 import get_req_params, return_response, headerfile_get_details, proxy_ids, get_cookie
import sys
import re
load_dotenv()
logger = get_logger("VOTER")

url = os.getenv("get_details")
origin = os.getenv("origin")
referer = os.getenv("referer")

def get_details(request):
    try:
        req = eval(request.data)  # the data we send in postman

        try:
            if ("epic" in req and "txnid" in req and "captcha" in req and "cookies" in req and "id" in req):
                epic = req["epic"]
                epic = epic.upper()
                txnid = req["txnid"]
                captcha = req["captcha"]
                captcha = captcha
                cookies = req["cookies"]
                cookies= cookies.upper()
                id = req["id"]
                id = id.upper()
            else:
                logger.error("...field not found(check for epic and txnid)...")
                return return_response(errors["FIELD_NOT_FOUND"])

        except Exception:
            logger.error("%s epic field not found %s",txnid,epic)
            return return_response(errors["FIELD_NOT_FOUND"])
        try:
            proxies = proxy_ids()
            print("proxy ip address", type(proxies))

            if str(req["epic"]) == "":
                logger.info("%s enter voter number... %s", txnid, epic)
                return return_response(errors["INVALID_VOTER_NUMBER"])

            v = "^[a-zA-Z]{3}[0-9]{7}$"
            if re.match(v, epic):
                logger.info(" %s is a valid voter number", epic)
            else:
                logger.error("%s voter regex dosen't match: %s", txnid, epic)
                return return_response(errors["INVALID_VOTER_NUMBER"])
            
            payload = json.dumps({
                        "isPortal": True,
                        "epicNumber": epic
                        })
            try:
                headers = headerfile_get_details(cookies, origin, referer)
                url = "https://gateway.eci.gov.in/api/v1/elastic/search-by-epic-from-national-display"
                try:
                    response = requests.request(
                        "POST", url, headers=headers, data=payload
                    )
                    try:
                        res = response.json()
                        res = dict(res[0])
                        data = dict({
                            "epic_number" : epic,
                            "name" : f'''{res['content']['applicantFirstName']} {res['content']['applicantLastName']} \n {res['content']['applicantFirstNameL1']} {res['content']['applicantLastNameL1']}''',
                            "age" : str(res['content']['age']),
                            "relative_name" :f'''{res['content']['relationName']} {res['content']['applicantLastName']} \n {res['content']['relationNameL1']} {res['content']['applicantLastNameL1']}''',
                            "state" : str(res['content']['stateName']),
                            "dist" : str(res['content']['districtValue']),
                            "polling_station" : str(res['content']['psbuildingName']),
                            "assembly_constituency" : str(res['content']['asmblyName']),
                            "parlimentary_constituency" : str(res['content']['districtValue'])
                        })
                        logger.info("%s success transaction of get details api:", txnid)
                        return return_response(errors["SUCCESS"], data)
                    except Exception:
                        logger.error("%s error at get details api: %s", txnid, sys.exc_info())
                        print("%s error at get details api:", txnid)
             
                except Exception:
                    logger.error("%s get details api request sent error: %s", txnid, sys.exc_info())
                    return return_response(errors["CONNECTION_ERROR"])
            except Exception:
                logger.error("%s internal error at cookie generation: %s", txnid, sys.exc_info())
                return return_response(errors["INTERNAL_ERROR"])
        except Exception:
            logger.error("%s invalid details at get details api: %s", txnid, sys.exc_info())
            return return_response(errors["INVALID_DETAILS"])
    except Exception:
        logger.error("%s bad request at get details api: %s", txnid, sys.exc_info())
        return return_response(errors["EMPTY_REQUEST_BODY"])






