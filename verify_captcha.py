import requests
import json
import os
from logging_helper import get_logger
from dotenv import load_dotenv
from error_file import errors
from utils_1 import  return_response, headerfile_verify, proxy_ids, get_cookie
import sys
import re
import base64
import random
from paddleocr import PaddleOCR


load_dotenv()
logger = get_logger("VOTER")

url = os.getenv("captcha_url")
origin = os.getenv("origin")
referer = os.getenv("referer")

def verify_captcha(request):
    try:
        req = eval(request.data)  # the data we send in postman

        try:
            if ("epic" in req and "txnid" in req and "captcha" in req and "cookies"in req and "cookies2"in req and "id" in req):
                epic = req["epic"]
                epic = epic.upper()
                txnid = req["txnid"]
                captcha = req["captcha"]
                cookies = req["cookies"]
                cookies2 = req['cookies2']
                id = req["id"]
            else:
                logger.error("...field not found(check for epic and txnid)...")
                return return_response(errors["FIELD_NOT_FOUND"])

        except Exception:
            logger.error("%s  epic field not found %s",txnid,epic)
            return return_response(errors["FIELD_NOT_FOUND"])

        try:
            proxies = proxy_ids()

            print("proxy ip address", type(proxies))

            # validations for epic
            if str(req["epic"]) == "":
                return return_response(errors["INVALID_VOTER_NUMBER"])

            v = "^[a-zA-Z]{3}[0-9]{7}$"
            if re.match(v, epic):
                logger.info(" %s is a valid voter number", epic)
            else:
                logger.error("%s voter regex dosen't match: %s", txnid, epic)
                return return_response(errors["INVALID_VOTER_NUMBER"])

            payload = {}
            try:
                # cookie = get_cookie()
                logger.info("%s -cookie generated: %s", txnid, cookies)
                headers = headerfile_verify(cookies, cookies2,origin,referer)
                try:
                    ocr = PaddleOCR(use_angle_cls=True, lang="en", use_gpu=False, show_log=False)

                    try:
                        captcha_name = f"captcha_{random.randint(8000,10000)}.jpg"
                        with open(captcha_name, "wb") as f:
                            f.write(base64.b64decode(captcha))
                        captcha_img = ocr.ocr(captcha_name, cls=False)[0][0][1][0]
                        os.remove(captcha_name)
                    except Exception:
                        os.remove(captcha_name)
                        return None

                        # print("captcha:",type(captcha), captcha)
                        # decoded_bytes = base64.b64decode(captcha)
                        # decoded_bytes= drive.execute_async_script
                        # Convert the bytes to text
                        # decoded_text = base64.b64decode(captcha).decode('utf-8')
                    url = f"https://gateway.eci.gov.in/api/v1/captcha-service/verifyCaptcha/{(str(captcha_img))}?id={id}"
                    
                    response = requests.request(
                        "POST", url, headers=headers, data=payload
                    )                    
                    res = response.json()
                    logger.info("%s -Second api request sent successfully: %s", txnid, res)
                    data = dict({"id": ""}) 
                    try:
                        id = res["id"]
                        data["id"] = id
                        data.update({"cookies": cookies})
                        data.update({"captcha" : captcha})
                        data.update({"cookies2":cookies2})
                        data.update({"txnid": txnid})
                        logger.info("%s success transaction of second api:", txnid)
                        return return_response(errors["SUCCESS"], data)
                    except Exception:
                        error_type = res["messages"][0]["desc"]

                        if error_type == "Exceeded limit" or len(error_type) > 50:
                            logger.error("%s: -error at login api: %s, %s",txnid,error_type,sys.exc_info())
                            return return_response({"respcode": 411, "respdesc": error_type})
                        else:
                            logger.error("%s -error at verify captcha api: %s", txnid, sys.exc_info())
                            return return_response({"respcode": 411, "respdesc": error_type})                            
                except Exception:
                    logger.error("%s verify captcha api request sent error: %s", txnid, sys.exc_info())
                    return return_response(errors["INTERNAL_ERROR"])
            except Exception:
                logger.error("%s internal error at cookie generation: %s", txnid, sys.exc_info())
                return return_response(errors["INTERNAL_ERROR"])
        except Exception:
            logger.error("%s invalid details at verify captcha api: %s", txnid, sys.exc_info())
            return return_response(errors["INVALID_DETAILS"])
    except Exception:
        logger.error("%s bad request at verify captcha api: %s", txnid, sys.exc_info())
        return return_response(errors["EMPTY_REQUEST_BODY"])
