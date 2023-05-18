import requests
import json
import os
from logging_helper import get_logger
from dotenv import load_dotenv
from error_file import errors
from utils_1 import  return_response
import sys
import re
from ast import literal_eval

load_dotenv()

logger = get_logger("VOTER")
url = os.getenv("url_search_by_epic")
origin = os.getenv("origin")
referer = os.getenv("referer")
server = os.getenv("SERVER")
port = os.getenv("API_VERSION_PORT")

def get_details2(epic, state, txnid):
    try:
        # req = eval(request.data)
        # epic = req["epic"]
        # epic = epic.upper()
        # txnid = req["txnid"]
        
        result = requests.request("POST",f"http:/{server}:{port}/get_captcha",headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "epic": epic,
                        "txnid": txnid
                
                    }))
        if result.json()["respdesc"] == "Success":
            # epic = result.join()['data']["epic"]
            # txnid = result.join()['data']["txnid"]
            captcha = result.json()["data"]["captcha"]
            cookies = result.json()["data"]["cookies"]
            cookies2 = result.json()["data"]["cookies2"]
            id = result.json()["data"]["id"]              
            result = requests.request("POST",f"http:/{server}:{port}/verify_captcha",headers={"Content-Type": "application/json"},
                data=json.dumps(
                    {
                        "epic": epic,
                        "txnid": txnid,
                        "captcha": captcha,
                        "cookies": cookies,
                        "cookies2":cookies2,
                        "id": id,
                    }
                ),
            )
            if result.json()["respdesc"] == "Success":
                
                captcha = result.json()["data"]["captcha"]
                cookies = result.json()["data"]["cookies"]
                cookies2 = result.json()["data"]["cookies2"]
                id = result.json()["data"]["id"] 
                result = requests.request("POST",f"http:/{server}:{port}/get_results",headers={"Content-Type": "application/json"},
                    data=json.dumps(
                        {
                            "epic": epic,
                            "captcha": captcha,
                            "cookies": cookies,
                            "txnid": txnid,
                            "id": id
                        }
                    ),
                )
                if result.json()["respdesc"] == "Success": 
                    # res = response.json()
                    # final_response = literal_eval(
                    # result.json()["data"],
                    # )
                    print("result:",result)
                    return result.json()
                else:
                    return result.json()
            else:
                    return result.json()
    except Exception:
        return return_response(errors["INTERNAL_ERROR"])
                        
