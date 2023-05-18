import sys
# from get_captcha import search_by_epic
from logging_helper import get_logger
from utils_1 import return_response, get_req_params
from error_file import errors
# from verify_captcha import verify_captcha
# from get_details import get_details
from internal_api import get_details2

logger = get_logger("voter_validation")

# def get_captcha_api(request):
#     try:
#         captcha_req_parms = get_req_params(request)
#         if captcha_req_parms == False:
#             return return_response(errors["INVALID_REQUEST"])

#         return search_by_epic(request)
#     except Exception :
#         logger.error("Global Error : %s", sys.exc_info())
#         return return_response(errors["EMPTY_REQUEST_BODY"])
    
# def verify_captcha_api(request):
#     try:
#         # verify_req_parms = verify_req_params(request)
#         if verify_req_parms == False:
#             return return_response(errors["INVALID_REQUEST"])

#         return verify_captcha(request)
#     except Exception :
#         logger.error("Global Error : %s", sys.exc_info())
#         return return_response(errors["EMPTY_REQUEST_BODY"])
    
# def get_details_api(request):
#     try:
#         get_req_params = verify_req_params(request)
#         if get_req_params == False:
#             return return_response(errors["INVALID_REQUEST"])
#         return get_details(request)
#     except Exception :
#         logger.error("Global Error : %s", sys.exc_info())
#         return return_response(errors["EMPTY_REQUEST_BODY"])
    
def get_details_api2(request):
    try:
        get_req_params1 = get_req_params(request)
        if get_req_params == False:
            return return_response(errors["INVALID_REQUEST"])
        return get_details2(request)
    except Exception :
        logger.error("Global Error : %s", sys.exc_info())
        return return_response(errors["EMPTY_REQUEST_BODY"])