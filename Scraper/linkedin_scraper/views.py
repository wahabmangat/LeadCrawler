from django.shortcuts import render,redirect
from django.http import HttpResponse
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium import webdriver
from datetime import datetime
import pandas as pd
import time
import re

from linkedin_scraper.models import ProfileData
from linkedin_scraper.utils import configure_webdriver
from linkedin_scraper.constants import LOGIN_URL
from linkedin_scraper.utils import start_new_thread
from linkedin_scraper.credentials import Email,Password

def request_url(driver, url):
    driver.get(url)

def append_data(data, field):
    data.append(str(field).strip("+"))

def login(driver, email, password):
    try:
        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located((By.ID, "username"))
        )
    except Exception as e:
        print(e)
        return False

    try:
        driver.find_element(By.ID, "username").click()
        driver.find_element(By.ID, "username").clear()
        driver.find_element(By.ID, "username").send_keys(email)

        driver.find_element(By.ID, "password").click()
        driver.find_element(By.ID, "password").clear()
        driver.find_element(By.ID, "password").send_keys(password)
        driver.find_element(By.CLASS_NAME, "btn__primary--large").click()
        time.sleep(5)
        not_logged_in = driver.find_elements(
            By.CLASS_NAME, "form__label--error")
        if len(not_logged_in) > 0:
            return False

        WebDriverWait(driver, 30).until(
            EC.presence_of_element_located(
                (By.CLASS_NAME, "global-nav__primary-item"))
        )
        return True

    except Exception as e:
        print(e)
        return False
    
def check_email(email):
    regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    if(re.fullmatch(regex, email)):
        return True
    else:
        return False
    
def find_data(driver, total_data, url):
    request_url(driver, url)
    scrapped_data=[]
    time.sleep(5)
    original_window = driver.current_window_handle
    driver.switch_to.new_window('tab')
    time.sleep(1)
    details_window = driver.current_window_handle
    error_count = 0
    while(1):
        driver.switch_to.window(original_window)
        time.sleep(3)
        try:
            profiles = driver.find_element(
                By.TAG_NAME, "main").find_element(
                By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
        except:
            print("Error Occurs")
        for profile in profiles:
            try:
                profile.location_once_scrolled_into_view
            except Exception as e:
                print(e)
        try:
            profiles = driver.find_element(
                By.TAG_NAME, "main").find_element(
                By.TAG_NAME, "ul").find_elements(By.TAG_NAME, "li")
        except:
            print("Error Occurs")
        for profile in profiles:
            try:
                data = []
                driver.switch_to.window(original_window)
                company = profile.find_element(By.CLASS_NAME, "entity-result__primary-subtitle").text.lower()
                if " at " in company:
                    company = company.split(" at ")[1]
                elif "@" in company:
                    company = company.split("@")[1]
                else:
                    company = company.split("ceo")[1]
                company_name = "N/A"
                if "\\" in company:
                    company_name = company.split("\\")[0]
                elif "|" in company:
                    company_name = company.split("|")[0]
                elif "/" in company:
                    company_name = company.split("/")[0]
                else:
                    company_name = company
                location = profile.find_element(By.CLASS_NAME, "entity-result__secondary-subtitle").text.lower()
                profile_link = profile.find_elements(By.CLASS_NAME, "app-aware-link")[0].get_attribute("href")
                driver.switch_to.window(details_window)
                driver.get(profile_link)
                time.sleep(3)
                complete_name = driver.find_element(By.TAG_NAME, "main").find_element(By.CLASS_NAME, "nAYezwEDADFmMdmotgdOJXPUZCEUgOAVc").find_element(By.TAG_NAME, "h1").text.lower()
                first_name = complete_name.split(" ")[0]
                last_name = complete_name.split(" ")[1]
                driver.find_element(By.CLASS_NAME, "ckIGrTtDdvzqEdmriOpcUZYyABFldJOY").find_element(By.TAG_NAME, "a").click()
                time.sleep(3)
                
                sections = driver.find_element(By.CLASS_NAME, "artdeco-modal__content").find_element(By.TAG_NAME, "ul")
                sections = sections.find_elements(By.TAG_NAME, "li")
                email = "Email not available"
                for section in sections:
                    temp = section.find_element(By.TAG_NAME, "p").text
                    temp = temp.split("\\")
                    for value in temp:
                        flag = check_email(value)
                        if flag:
                            email = value
                            break
                append_data(data, first_name)
                append_data(data, last_name)
                append_data(data, email)
                append_data(data, company_name)
                append_data(data, location)
                append_data(data, profile_link)
                scrapped_data.append(data)
                total_data += 1
            except Exception as e:
                print(e)
        # Get Pagination
        try:
            driver.switch_to.window(original_window)
            time.sleep(5)
            driver.find_element(By.CLASS_NAME, "artdeco-pagination").find_elements(By.TAG_NAME, "button")[-1].click()
            if total_data > 100:
                return scrapped_data
        except:
            error_count += 1
            if error_count > 7 :
                return scrapped_data
        
    
    
    

def index(request):
    return render(request, 'home.html')

def profiles(request):
    profiles = ProfileData.objects.all()
    return render(request, 'show_profiles.html',{'profiles':profiles})

def scrape(request):
    start_script()
    return redirect("index")

@start_new_thread
def start_script():
    total_data = 0
    try:
        driver = configure_webdriver(True)
        driver.maximize_window()
        request_url(driver, LOGIN_URL)
        email = Email
        password = Password
        
        logged_in = login(driver,email , password)
        try:
            if logged_in:
                url = "https://www.linkedin.com/search/results/people/?industry=%5B%2296%22%5D&keywords=ceo&origin=FACETED_SEARCH&sid=fr%3B"
                scraped_data = find_data(driver, total_data, url)
                user_profiles = [ProfileData(first_name=profile[0], last_name=profile[1], email=profile[2], company_name=profile[3], location=profile[4], url=profile[5]) for profile in scraped_data]
                ProfileData.objects.bulk_create(user_profiles, ignore_conflicts=True)
                print("SCRAPING_ENDED")
                driver.quit()
            else:
                print("LOGIN_FAILED")
                driver.quit()
        except Exception as e:
            print("Exception in linkedin => ", str(e))
            driver.quit()
    except Exception as e:
        print(e)
