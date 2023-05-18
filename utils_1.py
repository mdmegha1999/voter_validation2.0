import os
import sys
from error_file import errors

from dotenv import load_dotenv
from flask import jsonify
import requests
from logging_helper import get_logger
load_dotenv()

logger = get_logger('VOTER_ID')
http_ip = os.getenv('proxy_http_ip')
https_ip = os.getenv('proxy_https_ip')
a = os.getenv('a')

def headerfile(cookies, origin,referer):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Origin': 'https://electoralsearch.eci.gov.in',
        'Referer': 'https://electoralsearch.eci.gov.in/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Cookie': f'{cookies}'
        }
    return headers

def headerfile_verify(cookies,cookies2,origin,referer):
    headers = {
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Connection': 'keep-alive',
        'Content-Length': '0',
        'Origin': 'https://electoralsearch.eci.gov.in',
        'Referer': 'https://electoralsearch.eci.gov.in/',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'sec-ch-ua-mobile': '?1',
        'sec-ch-ua-platform': '"Android"',
        'Cookie': f'{cookies2}; {cookies}'
    }

    return headers

def headerfile_get_details(cookies,origin,referer):
    headers = {
        'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
        'Accept': 'application/json, text/plain, */*',
        'Content-Type': 'application/json',
        'Referer': 'https://electoralsearch.eci.gov.in/',
        'sec-ch-ua-mobile': '?1',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Mobile Safari/537.36',
        'sec-ch-ua-platform': '"Android"',
        'Cookie': f'{cookies}'
        }

    return headers

def return_response(error_code, data = None):
    """
    Returns jsonified resonse with result as key and output as value.
    """
    error_code.update({"data": data})
    return jsonify(error_code) 

def get_req_params(request):
    
    try:
        req = request.json
        logger.info("request : %s", req)
        epic = req["epic"]
        txnid = req["txnid"]
        # state = req["state"]
        if txnid == "" or epic == "" :
            return False
        return txnid, epic

    except Exception:
        logger.error("validating request params : %s", sys.exc_info())
        return False
    
# def verify_req_params(request):
#     try:
#         req = request.json
#         logger.info("request : %s", req)

#         epic = req["epic"]
#         txnid = req["txnid"]
#         captcha = req["captcha"]
#         cookies = req["cookies"]
#         cookies2 = req["cookies2"]
#         id = req["id"]

#         if txnid == "" or epic == "" or captcha == "" or cookies == "" or cookies2 == "" or id == "" :
#             return False
#         return txnid, epic, captcha, cookies, cookies2, id

#     except Exception:
#         logger.error("validating request params : %s", sys.exc_info())
#         return False
    
# def get_details_req_params(request):
#     try:
#         req = request.json
#         logger.info("request : %s", req)

#         epic = req["epic"]
#         txnid = req["txnid"]
#         captcha = req["captcha"]
#         cookies = req["cookies"]
#         cookies2 = req["cookies2"]

#         id = req["id"]

#         if txnid == "" or epic == "" or captcha == "" or cookies2 == "" or cookies == "" or id == "" :
#             return False
#         return txnid, epic, cookies, cookies2

#     except Exception:
#         logger.error("validating request params : %s", sys.exc_info())
#         return False
    
def get_cookie():
    try:
        session = requests.Session()          
        response = session.get('https://gateway.eci.gov.in/api/v1/elastic/search-by-epic-from-national-display')
        cookie_res = response.cookies.get_dict().items()
        new_list = []
        for x in cookie_res:
            new_list.append(x)
            return f"cookiesession1={new_list[0][1]}"

    except Exception:
        logger.info(session.cookies.get_dict())
        return return_response(errors["CONNECTION_ERROR"])

def proxy_ids():
    proxies = {
        'http':http_ip,
        'https':https_ip
        }

    return proxies





