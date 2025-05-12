from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import logging
import requests
import os

# print(f"https{gender}vidhika")

#setting up driver and opening chrome 
def setup_flipkart_driver(text,output_folder,logger,price_query,mini,maxi):
    try:
        main_results = []
        for dress in text["dress_types"]:
            if type(dress) == list:
                # print("💗checkpoint")
                for i, x in enumerate(dress):
                    results = []
                    chrome_options = webdriver.ChromeOptions()
                    prefs = {'download.default_directory': output_folder,
                             "download.prompt_for_download": False,
                             "safebrowsing.enabled": True}

                    chrome_options.add_experimental_option('prefs', prefs)
                    driver = webdriver.Chrome(options=chrome_options)
                    #search URL for flip
                    search_term = x.replace(" ", "+")
                    url = f"https://www.flipkart.com/search?q={search_term}&p%5B%5D=facets.price_range.from%3D{mini}&p%5B%5D=facets.price_range.to%3D{maxi}"
                    driver.get(url)
                    logger.info(f"Flipkart page loaded for {x}")
                    results.append(flipkart_extract(driver,logger))
                    main_results.append(results)
        print(main_results)
        return driver, main_results

    except Exception as e:
        logger.error(f"Error setting up Flipkart WebDriver: {e}")
        raise

#extracting the dresses from flipkart this time
def flipkart_extract(driver,logger):
    print("💗checkpoint 2 💗")
    try:
        # Wait for product containers to load
        # print("1 🥰")
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "_1sdMkc"))
        )
        # print("2 🥰")
        products = driver.find_elements(By.CLASS_NAME, "_1sdMkc")
        products = products[:3]
        # if products:
        #     print("3 🥰")
        #     print(len(products))
        # else:
        #     print("3 🥹")
        results = []
        for i,product in enumerate(products):
            try:
                
                # Image
                img_elem = product.find_element(By.CSS_SELECTOR, "img")
                image_url = img_elem.get_attribute("src")
                
                # Product link
                product_link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")
                # product_link = link_elem.get_attribute("href")
                if not product_link.startswith("http"):
                    product_link = "https://www.flipkart.com" + product_link

                # Name
                # name_elem = product.find_element(By.CSS_SELECTOR, "div._4rR01T, a.IRpwTa, a.s1Q9rs")
                # product_name = name_elem.text
                product_name=product.find_element(By.CLASS_NAME,"syl9yP").text
                product_desc = product.find_element(By.CLASS_NAME, "WKTcLC").text
                product_price=product.find_element(By.CLASS_NAME, "Nx9bqj").text

                # Price
                # price_elem = product.find_element(By.CSS_SELECTOR, "div._30jeq3")
                # product_price = price_elem.text

                # results.append({
                #     "name": product_name,
                #     "price": product_price,
                #     "image_url": image_url,
                #     "product_link": product_link
                # })
                product_data={
                    "name": product_name,
                    "description": product_desc,
                    "price": product_price,
                    "image_url": image_url,
                    "product_link": product_link
                }

                results.append(product_data)
                logger.info(f"Extracted Flipkart product {i+1}")
            except Exception as e:
                logger.error(f"Error extracting Flipkart product: {e}")
                continue
        logger.info(f"Successfully extracted {len(results)} Flipkart products")
        return results
    except Exception as e:
        logger.error(f"Error in flipkart_extract: {e}")
        return []
    
def executeFlipkartBase(text):
    #setup paths
    output_folder = "Outputs\dress_type_images"
    os.makedirs(output_folder, exist_ok=True)

    #setting up logging for keeping a track of all the the events when this program runs
    logging.basicConfig(filename="bot_log.log",format="%(asctime)s - %(message)s",level=logging.DEBUG)
    logger=logging.getLogger()
    
    mini=text["price_range"]["min_range"]
    maxi=text["price_range"]["max_range"]
    price_query= f"rf=Price%3A{mini}.0_{maxi}.0_{mini}.0%20TO%20{maxi}.0"
    _,results=setup_flipkart_driver(text,output_folder,logger,price_query,mini,maxi)
    return results