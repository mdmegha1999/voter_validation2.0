import requests
import json
import os
from logging_helper import get_logger
from dotenv import load_dotenv
from error_file import errors
from utils_1 import get_req_params, return_response, headerfile, proxy_ids, get_cookie
import sys
import re

load_dotenv()

logger = get_logger("VOTER")
url = os.getenv("url_search_by_epic")
origin = os.getenv("origin")
referer = os.getenv("referer")

def search_by_epic(request):
    try:
        req = eval(request.data)  # the data we send in postman
        try:
            if "epic" in req and "txnid" in req:
                epic = req["epic"]
                epic = epic.upper()
                txnid = req["txnid"]
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
                logger.error("%s enter voter number... %s", txnid, epic)
                return return_response(errors["INVALID_VOTER_NUMBER"])

            v = "^[a-zA-Z]{3}[0-9]{7}$"
            if re.match(v, epic):
                logger.info(" %s is a valid voter number", epic)
            else:
                logger.error("%s voter regex dosen't match: %s", txnid, epic)
                return return_response(errors["INVALID_VOTER_NUMBER"])

            payload = {}
            try:
                cookies = get_cookie()
                logger.info("%s -cookie generated: %s", txnid, cookies)
                headers = headerfile(cookies,origin, referer)
                url = "https://gateway.eci.gov.in/api/v1/captcha-service/generateCaptcha"
                try:
                    response = requests.request(
                        "GET", url, headers=headers, data=payload
                    )
                    cookie_header = response.headers['set-cookie']
                    res = response.json()
                    
                    data = dict({"id": ""}) 

                    try:
                        captcha = res["captcha"]
                        id = res["id"]
                        data["id"] = id
                        data.update({"cookies": cookies})
                        data.update({"captcha" : captcha})
                        data.update({"cookies2":cookie_header})
                        data.update({"txnid": txnid})
                        logger.info("%s success transaction of first api:", txnid)
                        return return_response(errors["SUCCESS"], data)
                    except Exception:
                        
                        error_type = res["messages"][0]["desc"]

                        if error_type == "Exceeded limit" or len(error_type) > 50:
                            logger.error("%s: -error at get captcha api: %s, %s",txnid,error_type,sys.exc_info())
                            return return_response({"respcode": 411, "respdesc": error_type})
                        else:
                            logger.error("%s -error at get captcha api: %s", txnid, sys.exc_info())
                            return return_response({"respcode": 411, "respdesc": error_type})                            

                except Exception:
                    logger.error("%s get captcha api request sent error: %s", txnid, sys.exc_info())
                    return return_response(errors["INTERNAL_ERROR"])
            except Exception:
                logger.error("%s internal error at cookie generation: %s", txnid, sys.exc_info())
                return return_response(errors["INTERNAL_ERROR"])
        except Exception:
            logger.error("%s invalid details at get captcha api: %s", txnid, sys.exc_info())
            return return_response(errors["INVALID_DETAILS"])
    except Exception:
        logger.error("%s bad request at get captcha api: %s", txnid, sys.exc_info())
        return return_response(errors["EMPTY_REQUEST_BODY"])
