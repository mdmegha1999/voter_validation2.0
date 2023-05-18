import sys
from asyncio.log import logger
from flask import jsonify
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from logging_helper import get_logger
from errors import errors

 
logger = get_logger("voter_validation")


def return_response(error_code, data=None):
    """
    Returns jsonified resonse with result as key and output as value.
    """
    error_code.update({"data": data})
    return jsonify(error_code)


def val_req_params(request):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    request: object

            Returns:
                    bool
    """
    try:
        req = request.json
        logger.info("request : %s", req)

        epic = req["epic"]
        state = req["state"]
        txnid = req["txnid"]
        return epic, state,txnid

    except Exception:
        logger.error("validating request params : %s", sys.exc_info())
        return return_response(errors["EMPTY_REQUEST_BODY"])



def safe_execute(try_condition, default=""):
    """_summary_

    Args:
        default (_type_): _description_
        exception (_type_): _description_
        function (_type_): _description_

    Returns:
        _type_: _description_
    """
    try:
        return try_condition
    except Exception:
        return default

def setup_chrome(url, txnid):
    """_summary_"""
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    logger.info("%s - intializing chrome", txnid)
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
    driver.get(url)
    logger.info("%s - opening website", txnid)
    driver.maximize_window()
    return driver

def get_chromedriver():
    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument("--headless")

    chrome_options.add_argument('--disable-blink-features=AutomationControlled')
    chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
    chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_argument("--start-maximized")
    user_agent = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.2 (KHTML, like Gecko) Chrome/22.0.1216.0 Safari/537.2'
    chrome_options.add_argument(f'user-agent={user_agent}')
    # chrome_options.add_experimental_option("prefs", {
    #     "download.prompt_for_download": False,
    #     "download.directory_upgrade": True,
    #     "safebrowsing_for_trusted_sources_enabled": False,
    #     "safebrowsing.enabled": False
    #     }
    # )
    driver = webdriver.Chrome(executable_path='./chromedriver', options=chrome_options)
    return driver
