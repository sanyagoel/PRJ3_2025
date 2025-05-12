from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
import requests
import os

# print(f"https{gender}vidhika")

#setting up driver and opening chrome 
def setup_driver(text,output_folder,logger,gender_query,price_query):
    try:
        main_results=[]
        for dress in text["dress_types"]:
            if type(dress)==list:
                print("💗checkpoint")
                for i,x in enumerate(dress):
                    results=[]
                    print(f"dress {i} in DRESS: ",x)
                    chrome_options = webdriver.ChromeOptions()
                    prefs = {'download.default_directory' : output_folder,
                            "download.prompt_for_download": False,
                            "safebrowsing.enabled": True}

                    chrome_options.add_experimental_option('prefs', prefs)
                    driver = webdriver.Chrome(options=chrome_options)
                    driver.get(f"https://www.myntra.com/{x}?&{gender_query}&rawQuery={x}&{price_query}")
                    logger.info(f"Page loaded")
                    results.append(myntra_extract(driver,logger))
                    main_results.append(results)
        # print("💗results: ",main_results)
        return driver,main_results
    
    except Exception as e:
        logger.error(f"Error setting up WebDriver: {e}")
        raise
    
    
#extracting the dresses from myntra
def myntra_extract(driver,logger):
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "product-base")))
        products = driver.find_elements(By.CLASS_NAME, "product-base")
        products = products[:3]
        results = []
        for i, product in enumerate(products):
            try:
                product_link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                image_element = product.find_element(By.CSS_SELECTOR, "img.img-responsive")
                image_url = image_element.get_attribute("src")
                
                product_name = product.find_element(By.CLASS_NAME, "product-brand").text
                product_desc = product.find_element(By.CLASS_NAME, "product-product").text
                product_price = product.find_element(By.CLASS_NAME, "product-discountedPrice").text
                
                product_data = {
                    "name": product_name,
                    "description": product_desc,
                    "price": product_price,
                    "image_url": image_url,
                    "product_link": product_link
                }
                
                results.append(product_data)
                logger.info(f"Extracted product {i+1}: {product_name}")
                
            except Exception as e:
                logger.error(f"Error extracting product {i+1}: {e}")
                continue
        
        logger.info(f"Successfully extracted {len(results)} products")
        print("💗checkpoint end for one dress")
        return results
        
        
    except Exception as e:
        logger.error(f"Error in myntra_extract: {e}")
        return []
    
def executeMyntraBase(text):
    #setup paths
    output_folder = "Outputs\dress_type_images"
    os.makedirs(output_folder, exist_ok=True)

    #setting up logging for keeping a track of all the the events when this program runs
    logging.basicConfig(filename="bot_log.log",format="%(asctime)s - %(message)s",level=logging.DEBUG)
    logger=logging.getLogger()
    
    if text["gender"]=="F":
        gender_query="f=Gender%3Amen%20women%2Cwomen"
    else:
        gender_query="f=Gender%3Aboys%2Cboys%20girls"
        
    mini=text["price_range"]["min_range"]
    maxi=text["price_range"]["max_range"]
    price_query= f"rf=Price%3A{mini}.0_{maxi}.0_{mini}.0%20TO%20{maxi}.0"
    _,results=setup_driver(text,output_folder,logger,gender_query,price_query)
    return results