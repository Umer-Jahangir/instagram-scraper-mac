#!/usr/bin/env python3

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from getpass import getpass
import os
import sys
import csv
import time
import random
import re
import platform
                                        
                                                         
profession=input("Enter Profession to Search (e.g., Singer, Musician, Band): ")
location=input("Enter The Specific Location: ")
category=input("Enter the Catgeory (eg:Hip-Hop, Rock): ")
# Configuration
QUERY =f"'site:instagram.com' '{profession}' '{location}' '{category}' 'gmail.com' "
OUTPUT_FILE = 'instagram_profiles.csv'
MAX_PAGES = 4 # None FOR ALL PAGES
DELAY_BETWEEN_PROFILES = (3, 7) 
#
INSTA_USERNAME = input("Enter your Instagram username: ")
INSTA_PASSWORD = getpass("Enter your Instagram password: ")

# Set up Chrome options
options = Options()
options.add_argument("--no-sandbox")
options.add_argument("--disable-blink-features=AutomationControlled")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--disable-infobars")
options.add_argument("--disable-extensions")
options.add_argument("--disable-popup-blocking")
options.add_argument("--disable-default-apps")
options.add_argument("--no-first-run")
options.add_argument("--disable-notifications")
options.add_argument("--disable-gpu")
options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36")
options.add_argument("--headless=new")  # Remove if you need a visible browser
options.add_argument("--start-maximized")
if platform.machine() == 'arm64':
    options.add_argument("--disable-features=RosettaTranslate")
    options.add_argument("--use-angle=metal")
if platform.machine() == 'x86_64':
    options.add_argument("--disable-gpu")
    
    
options.binary_location = "/Applications/Chromium.app/Contents/MacOS/Chromium"


# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
driver = webdriver.Chrome(options=options)
wait = WebDriverWait(driver, 15)

def login_to_instagram():
    """Login to Instagram before scraping"""
    print("\nLogging into Instagram...")
    driver.get("https://www.instagram.com/")
    time.sleep(random.uniform(2, 4))
    
    # Accept cookies if popup appears
    try:
        cookie_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Allow essential and optional cookies')]")))
        cookie_button.click()
        time.sleep(1)
    except:
        pass
    
    # Fill login form
    username_field = wait.until(EC.presence_of_element_located((By.NAME, "username")))
    password_field = driver.find_element(By.NAME, "password")
    
    username_field.send_keys(INSTA_USERNAME)
    password_field.send_keys(INSTA_PASSWORD)
    password_field.send_keys(Keys.RETURN)
    time.sleep(random.uniform(3, 5))
    
    # Handle "Save Info" prompt
    try:
        not_now_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[contains(text(), 'Not Now')]")))
        not_now_button.click()
        time.sleep(1)
    except:
        pass
    
    # Verify login success
    if "accounts/login" in driver.current_url:
        print("Login failed! Please check your credentials.")
        driver.quit()
        exit()
    else:
        print("Successfully logged in to Instagram")

def is_profile_url(url):
    """Check if URL is an Instagram profile URL (not post/reel/explore/etc)"""
    # if not url or "instagram.com" not in url:
    #     return False
    
    exclude_patterns = [
        '/p/', '/reel/', '/tv/', '/explore/', '/stories/',
        '/accounts/', '/direct/', '/tags/', '/location/',
        '/reels/', '/highlight/', '/channel/', '/guide/'
    ]
    
    if any(pattern in url for pattern in exclude_patterns):
        return False
    
    path_parts = [p for p in url.split('instagram.com/')[1].split('/') if p]
    return len(path_parts) == 1 and '.' not in path_parts[0]

def scrape_google_results():
    """Scrape Instagram profile URLs from Google search results"""
    print("\nStarting Google search...")
    driver.get("https://www.google.com")
    time.sleep(random.uniform(2, 4))
    
    # Accept cookies if present
    try:
        cookie_button = wait.until(EC.element_to_be_clickable(
            (By.XPATH, "//button[div[contains(text(),'Accept all')]]")))
        cookie_button.click()
        time.sleep(1)
    except:
        pass  
    
    # Perform search
    search_box = wait.until(EC.presence_of_element_located((By.NAME, "q")))
    search_box.clear()
    
    for char in QUERY:
        search_box.send_keys(char)
        time.sleep(random.uniform(0.1, 0.3))
    search_box.send_keys(Keys.RETURN)
    time.sleep(random.uniform(2, 4))
    
    profile_urls = set()
    page_num = 1
    
    while True:
        if MAX_PAGES and page_num > MAX_PAGES:
            break
            
        print(f"Processing Google page {page_num}...")
        
        wait.until(EC.presence_of_element_located((By.ID, "search")))
        
        # Scroll to load all results
        last_height = driver.execute_script("return document.body.scrollHeight")
        while True:
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(random.uniform(1, 2))
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
        
        # Extract all links
        links = driver.find_elements(By.XPATH, "//div[@id='search']//a[not(contains(@href, 'google.com')) and @href]")        
        new_urls = 0
        for link in links:
            try:
                url = link.get_attribute("href")
                if is_profile_url(url):
                    username = url.split('instagram.com/')[1].split('/')[0].split('?')[0]
                    profile_url = f"https://www.instagram.com/{username}/"
                    if profile_url not in profile_urls:
                        profile_urls.add(profile_url)
                        new_urls += 1
            except Exception as e:
                print(f"Error processing link: {e}")
                continue
        
        print(f"Found {new_urls} new profiles (Total: {len(profile_urls)})")
        
        # Try next page
        try:
            next_button = driver.find_element(By.XPATH, "//a[@id='pnnext']")
            driver.execute_script("arguments[0].click();", next_button)
            page_num += 1
            time.sleep(random.uniform(2, 4))
        except NoSuchElementException:
            print("No more pages found")
            break
        except Exception as e:
            print(f"Error going to next page: {e}")
            break
    
    return list(profile_urls)

def scrape_instagram_profile(url):
    """Scrape public information from Instagram profile"""
    print(f"\nScraping: {url}")
    driver.get(url)
    time.sleep(random.uniform(*DELAY_BETWEEN_PROFILES))
    
    # Check if we got logged out
    if "accounts/login" in driver.current_url:
        print("Detected login page, re-authenticating...")
        login_to_instagram()
        driver.get(url)
        time.sleep(random.uniform(*DELAY_BETWEEN_PROFILES))
    
    try:
        wait.until(EC.presence_of_element_located((By.TAG_NAME, "header")))
        username = url.split("/")[-2]
        full_name = ""
        first_name = ""
        last_name = ""
        bio = ""
        email = ""
        acc_type = ""
        
        try:
            full_name = driver.find_element(By.XPATH, "//header//span[contains(@class,'_aaco') and contains(@class,'_aacu')]").text.strip()
            # Split full name into first and last names
            name_parts = full_name.split()
            first_name = name_parts[0] if len(name_parts) > 0 else ""
            last_name = " ".join(name_parts[1:]) if len(name_parts) > 1 else ""
        except:
            pass
        try:
            more_button = driver.find_element(By.XPATH, "//span[text()='more']")
            more_button.click()
        except:
            pass  # No "more" button found
        
        bio_elm = driver.find_element(By.XPATH, '//span[@class="_ap3a _aaco _aacu _aacx _aad7 _aade"][@dir="auto"]')
        bio=bio_elm.text
        try:
            emails = re.findall(r'[\w\.-]+@[\w\.-]+\.\w+', bio)
            if emails:
              email = emails[0]  # Get the first email if multiple
              print("Email:", email)
            else:
               print("No email found")
        except:
            print("some logical")
        try:
            bio = driver.find_element(By.XPATH, "//header//span[contains(@class,'_aaco') and contains(@class,'_aacu')]/following-sibling::span").text.strip()
            email_match = re.search(r'[\w\.-]+@[\w\.-]+', bio)
            if email_match:
                email = email_match.group(0)
        except:
            pass
        
        try:
            acc_type = driver.find_element(By.XPATH, "//header//div[contains(text(),'Verified') or contains(text(),'Business')]").text
        except:
            acc_type = "Personal"
        
        return {
            "url": url,
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "bio": bio,
            "email": email,
            "account_type": acc_type,
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        print(f"Error scraping profile: {e}")
        return None

def main():
    # First login to Instagram
    login_to_instagram()
    
    profile_urls = scrape_google_results()
    
    if not profile_urls:
        print("No Instagram profiles found!")
        driver.quit()
        return
    
    print(f"\nFound {len(profile_urls)} Instagram profiles. Starting profile scraping...")
    
    # Prepare CSV file
    with open(OUTPUT_FILE, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['url', 'username', 'first_name', 'last_name', 'bio', 'email', 'account_type', 'timestamp']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Scrape each profile
        success_count = 0
        for url in profile_urls:
            profile_data = scrape_instagram_profile(url)
            if profile_data:
                writer.writerow(profile_data)
                success_count += 1
                print(f"Saved: {profile_data['username']}")
            
            time.sleep(random.uniform(*DELAY_BETWEEN_PROFILES))
    
    print(f"\nScraping complete! Successfully scraped {success_count}/{len(profile_urls)} profiles.")
    print(f"Results saved to {OUTPUT_FILE}")

if __name__ == "__main__":
    try:
        main()
    finally:
        driver.quit()
