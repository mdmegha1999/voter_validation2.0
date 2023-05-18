import os
import sys
from captcha_solver import solve_captcha
from dotenv import load_dotenv
from selenium.webdriver import ActionChains
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver import ActionChains
from logging_helper import get_logger
from utils import return_response, safe_execute
from utils import setup_chrome
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from errors import errors
load_dotenv()

url = os.getenv("new_voter_url")
logger = get_logger("voter_validation")

def vv_scraper_api(epic,txnid):
    driver = setup_chrome(url, txnid)
    try:
        search_epic_xpath = '//*[@id="epic"]/p'
        epic_no_xpath ='//*[@id="epicID"]'
        # state_xpath = '//*[@id="epicStateList"]'
        captcha_image_xpath ='/html/body/div/div[2]/div/div[3]/div[3]/div[1]/div[1]/div[1]/div/img'
        captcha_input_xpath ='//*[@id="root"]/div[2]/div/div[3]/div[3]/div[1]/div/div[2]/div[2]/div/input'
        captcha_submit_xpath = '//*[@id="root"]/div[2]/div/div[3]/div[3]/div[1]/div/button'
        validate_success_xpath = '//*[@id="root"]/div[2]/div/div[3]/div[3]/div[2]/button[1]'
        view_details_xpath = '//*[@id="style-2"]'
        try:
            # search_epic_element =  WebDriverWait(driver, 2).until(
            #     EC.presence_of_element_located((By.XPATH, search_epic_xpath))
            # )
            search_epic_element = driver.find_element(By.XPATH, search_epic_xpath).click()
            sleep(2)
        except Exception:
            logger.error("Invalid Voter Number By Searche : %s", sys.exc_info())
            return return_response(errors["INVALID_REQUEST"])
        try:
            epic_input_element =  WebDriverWait(driver, 5).until(
                EC.presence_of_element_located((By.XPATH, epic_no_xpath))
            )
            epic_input_element.send_keys(epic)
            sleep(2)
        except Exception:
            logger.error("Invalid epic Number : %s", sys.exc_info())
            return return_response(errors["INVALID_REQUEST"])
        
        # try:
        #     state_xpath = '//*[@id="epicStateList"]'
        #     driver.find_element(By.XPATH, state_xpath).click()
        #     state_element = driver.find_element(By.XPATH, state_xpath).text

        #     state_list = state_element.split('\n')
        #     # converted_desired_month = int(desired_month)
        #     desired_state = state
        #     state_index = None
        #     # converted_desired_state = int(desired_state)

        #     # res = state_list[converted_desired_state-1]
        #     # state_index = None
        #     for i, state in enumerate(state_list):
        #         if state.lower() == desired_state.lower():
        #             state_index = i
        #             break
        #     if state_index is not None:
        #         select_opt = driver.find_element(By.XPATH,'//*[@id="epicStateList"]')
        #         select_opt.find_elements(By.TAG_NAME, 'option')[state_index].click()
        #         sleep(1)
            
        # except Exception:
        #     logger.error("Invalid voter Number : %s", sys.exc_info())
        #     return return_response(errors["INVALID_REQUEST"])
        
        
        
    # Captcha solving
        try:
            logger.info("%s solving captcha", txnid)
            captcha_process = solve_captcha(
                driver,
                txnid,
                captcha_image_xpath,
                captcha_input_xpath,
                captcha_submit_xpath,
                validate_success_xpath,
                3   
            )
            if captcha_process == False:
                driver.quit()
                return return_response(errors["INTERNAL_ERROR"])
        except Exception:
            logger.error("solving captcha : %s", sys.exc_info())
            driver.quit()
            return return_response(errors["INTERNAL_ERROR"])
        try:
            view_details = WebDriverWait(driver, 2).until(
            EC.element_to_be_clickable((By.XPATH, view_details_xpath)))
            view_details.click()
            try:
                WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.XPATH, '/html/body/div[4]/div/div[1]')))
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
            logger.error("Invalid voter Number : %s", sys.exc_info())
            return return_response(errors["INVALID_REQUEST"])
        
    except Exception:
        logger.error("global error voter : %s", sys.exc_info())
        driver.quit()
        return return_response(errors["INTERNAL_ERROR"])
        
