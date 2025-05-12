from selenium import webdriver
import logging
from datetime import datetime, timedelta

import requests
import time
import os
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# # Setup paths
# output_folder = "dress_type_images"
# os.makedirs(output_folder, exist_ok=True)

# #setting up logging for keeping a track of all the the events when this program runs
# logging.basicConfig(filename="bot_log.log",format="%(asctime)s - %(message)s",level=logging.DEBUG)
# logger=logging.getLogger()

# output_folder= "./Outputs"
# files = r'outputs' 
# if not os.path.exists(files):
#     os.makedirs(files)

# text={"dress types":['navy saree', 'red chaniya choli', ['purple embroidered floor-length salwar kameez'], 'green intricately designed kurti with matching pyjama', 'beige embroidered long kaftan'],
#       "price range": {"min_range":4500, "max_range":6400},
#       "gender": "F"}

# # print(len(text["dress types"]))
# dress_query=[]
# for i in text["dress types"]:
#     dress_query.append(i)
#     # print(i)

# if text["gender"]=="F":
#     gender_query="f=Gender%3Amen%20women%2Cwomen"
# else:
#     gender_query="f=Gender%3Aboys%2Cboys%20girls"
    
# mini=text["price range"]["min_range"]
# maxi=text["price range"]["max_range"]
# price_query= f"rf=Price%3A{mini}.0_{maxi}.0_{mini}.0%20TO%20{maxi}.0"

# print(f"https{gender}vidhika")

logging.basicConfig(filename="bot_log.log",format="%(asctime)s - %(message)s",level=logging.DEBUG)
logger=logging.getLogger()

#setting up driver and opening chrome 
def setup_driver(text, output_folder):
    try:
        # # Prepare gender and price query
        # if text["gender"] == "F":
        #     gender_query = "f=Gender%3Amen%20women%2Cwomen"
        # else:
        #     gender_query = "f=Gender%3Aboys%2Cboys%20girls"
        
        mini = text["price range"]["min_range"]
        maxi = text["price range"]["max_range"]
        # price_query = f"rf=Price%3A{mini}.0_{maxi}.0_{mini}.0%20TO%20{maxi}.0"

        for dress in text["dress types"]:
            if type(dress) == list:
                for i, x in enumerate(dress):
                    chrome_options = webdriver.ChromeOptions()
                    prefs = {'download.default_directory': output_folder,
                             "download.prompt_for_download": False,
                             "safebrowsing.enabled": True}
                    chrome_options.add_experimental_option('prefs', prefs)
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.maximize_window()
                    # --- Build the full Myntra URL with filters ---
                    url = f"https://www.myntra.com/{x}"
                    driver.get(url)
                    logger.info(f"Page loaded: {url}")
                    pic_extract(driver, x, output_folder, text)
            else:
                chrome_options = webdriver.ChromeOptions()
                prefs = {'download.default_directory': output_folder,
                         "download.prompt_for_download": False,
                         "safebrowsing.enabled": True}
                chrome_options.add_experimental_option('prefs', prefs)
                driver = webdriver.Chrome(options=chrome_options)
                driver.maximize_window()
                url = f"https://www.myntra.com/{dress}"
                driver.get(url)
                logger.info(f"Page loaded: {url}")
                pic_extract(driver, dress, output_folder, text)
        return driver

    except Exception as e:
        logger.error(f"Error setting up WebDriver: {e}")
        raise

    
#extracting the dresses from myntra

def pic_extract(driver,x, output_folder, text):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-base")))
        products = driver.find_elements(By.CLASS_NAME, "product-base")
        product = products[0]
        image_element = product.find_element(By.CSS_SELECTOR, "img.img-responsive")
        image_url = image_element.get_attribute("src")
        if image_url:
            img_data = requests.get(image_url).content
            filename = f"{output_folder}/{x.lower().replace(' ', '_')}.jpg"
            with open(filename, "wb") as f:
                f.write(img_data)
                logger.info(f"Downloaded image for: {x}")
                print(f"Downloaded image for: {x}")
        else:
            logger.error(f"No image found for: {x}")
            print(f"No image found for: {x}")
                
        
        logger.info(f"Successfully extracted {len(text['dress types'])} outfit types")
        return
        
    except Exception as e:
        logger.error(f"Error in extract iamges: {e}")
        return []

        

def executeBase(text):
    
    output_folder = "./Outputs/dress_type_images"
    os.makedirs(output_folder, exist_ok=True)

    #setting up logging for keeping a track of all the the events when this program runs

    # output_folder= "./Outputs"
    files = r'outputs' 
    if not os.path.exists(files):
        os.makedirs(files)

    # text={"dress types":['navy saree', 'red chaniya choli', ['purple embroidered floor-length salwar kameez'], 'green intricately designed kurti with matching pyjama', 'beige embroidered long kaftan'],
    #     "price range": {"min_range":4500, "max_range":6400},
    #     "gender": "F"}

    # print(len(text["dress types"]))
    dress_query=[]
    for i in text["dress types"]:
        dress_query.append(i)
        # print(i)

    # if text["gender"]=="F":
    #     gender_query="f=Gender%3Amen%20women%2Cwomen"
    # else:
    #     gender_query="f=Gender%3Aboys%2Cboys%20girls"
        
    # mini=text["price range"]["min_range"]
    # maxi=text["price range"]["max_range"]
    # price_query= f"rf=Price%3A{mini}.0_{maxi}.0_{mini}.0%20TO%20{maxi}.0"
    
    setup_driver(text, output_folder)
