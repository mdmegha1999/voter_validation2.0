import sys
from s_scraper import vv_scraper_api
# from voter_val import vv_scraper_api

from logging_helper import get_logger
from utils import return_response, val_req_params
from errors import errors
from time import sleep
from time import time 
import re
from internal_api import get_details2

logger = get_logger("voter_validation")

def voter_validation_api(request):
    try:
        req_parms = val_req_params(request)
        if req_parms == False:
            return return_response(errors["INVALID_REQUEST"])
        epic,state, txnid= req_parms
        if state in ['Karnataka', 'Maharashtra', 'Meghalaya', 'Nagaland', 'Tripura', 'Uttar Pradesh', 'West Bengal','Lakshadweep', 'Jammu and Kashmir' 'Ladakh' ]:
            return vv_scraper_api(epic,state, txnid)
        else: 
            return get_details2(epic, state, txnid)
    except Exception as ex:
        logger.error("Global Error : %s", ex)
        return return_response(errors["EMPTY_REQUEST_BODY"])
    