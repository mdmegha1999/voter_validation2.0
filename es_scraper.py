"""
Scraper function for parivahan website -selenium

Functions:

    p_scraper_api(txnid, dlno, dob) -> object

"""
import os
import sys
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from dotenv import load_dotenv
from time import sleep
from errors import errors
import xpaths_directory as xd
from captcha_solver import solve_captcha
from utils import return_response, safe_execute,get_chromedriver
from logging_helper import get_logger

load_dotenv()

url = os.getenv("NVSP")


logger = get_logger("voter_validation")



def es_scraper_api(voter_no,txnid):
    """
    Returns the dl_validation_api function return value as API response.

            Parameters:
                    txnid: int
                    dlno: string
                    dob: string

            Returns:
                    value as API response
    """
    try:
        # driver = setup_chrome(url, txnid)
        driver= get_chromedriver()
        logger.info(f'{txnid} => Opening Website')
            

        driver.get(url)
        try:
            # WebDriverWait(driver, 10).until(
            #             EC.presence_of_element_located((By.XPATH, '//*[@id="continue"]'))).click()
        
            WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, '/html/body/div[8]/div[2]/div/div/div/input'))).click()
            print("continue clicked...")
        except Exception:
            pass

        # Search_by_EPIC = WebDriverWait(driver, 2).until(
        #             EC.presence_of_element_located((By.XPATH, '//*[@id="mainContent"]/div[2]/div/div/ul/li[2]')))
        
        Search_by_EPIC = WebDriverWait(driver, 4).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/div/div/ul/li[2]'))) 
        Search_by_EPIC.click()
        print("1")
        # search_uid_elem = WebDriverWait(driver, 2).until(
        #             EC.presence_of_element_located((By.XPATH, '//*[@id="name"]')))

        search_uid_elem = WebDriverWait(driver, 2).until(
                    EC.presence_of_element_located((By.XPATH, '/html/body/div[4]/div[3]/div/div/div[2]/form/fieldset/div[1]/div/div[2]/input')))        
        print("2")        
        # Enter EPIC number in the input box
        search_uid_elem.send_keys(voter_no)

        logger.info("%s solving captcha", txnid)
        captcha_process = solve_captcha(
            driver, txnid, xd.ESCI, xd.ESCII, xd.ESCS, xd.ESVS, logger
        )

        print("captche result:",captcha_process)
        if captcha_process == False or captcha_process==None:
            try:
                WebDriverWait(driver, 1).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[1]/div/div[1]')))
                logger.error("%s No details found:", txnid)
                driver.quit()
                return return_response(errors["DETAILS_NOT_FOUND"])
            except Exception: 
                logger.error("%s invalid captcha:", txnid)
                driver.quit()
                return return_response(errors["INTERNAL_ERROR"])
        # sleep(1)
        try:
            view_details = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, '/html/body/div[5]/div[3]/div[2]/div/table/tbody/tr/td[1]/form/input[25]')))
            view_details.click()
            try:
        
                WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]')))
                # driver.execute_script("window.scrollBy(0, 250)")
                # sleep(1)
                # driver.execute_script("window.scrollBy(0, 250)")
                data = {
                    "epic_number" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[2]').text.strip()),
                    "name" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[3]').text.strip()),
                    "age" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[4]').text.strip()),
                    "relative_name" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[5]').text.strip()),
                    "state" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[6]').text.strip()),
                    "dist" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[7]').text.strip()),
                    "polling_station" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[8]').text.strip()),
                    "assembly_constituency" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[9]').text.strip()),
                    "parlimentary_constituency" : str(driver.find_element( "xpath",'//*[@id="resultsTable"]/tbody/tr/td[10]').text.strip())
                }
       
                logger.info("%s => Success transaction", txnid)
                driver.quit()
                return return_response(errors["SUCCESS"], data)
            except Exception:
                logger.error("%s details fetching failed : %s", txnid, sys.exc_info())
                driver.quit()
                return return_response(errors["DETAILS_FETCHING_FAILED"])
        except Exception:
            logger.error("%s Internal error occurred: %s", txnid, sys.exc_info())
            driver.quit()
            return return_response(errors["INTERNAL_ERROR"])
    except Exception:
        logger.error("%s Internal error occurred : %s", txnid, sys.exc_info())
        driver.quit()
        return return_response(errors["INTERNAL_ERROR"])


