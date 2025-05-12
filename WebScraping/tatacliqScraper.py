from selenium import webdriver
import logging
import os
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote

def build_tatacliq_url(search_term, min_price, max_price, gender_query):
    price_str = f"₹{min_price:,}-₹{max_price:,}"
    print(gender_query)
    
    params = [search_term, "relevance", "inStockFlag:true",f"category:{gender_query}",f"price:{price_str}"]
    url = "https://www.tatacliq.com/search/?q=" + quote(":".join(params))
    return url

def setup_tatacliq_driver(text,output_folder,logger,gender_query,mini,maxi):
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
                    url = build_tatacliq_url(x, mini, maxi, gender_query)
                    print(f"URL: {url}")
                    driver.get(url)
                    logger.info(f"Tata CLiQ page loaded for {x}")
                    results.append(tatacliq_extract(drive,logger))
                    main_results.append(results)
        print(main_results)
        quit(driver)
        return driver, main_results

    except Exception as e:
        logger.error(f"Error setting up Tata CLiQ WebDriver: {e}")
        raise

def tatacliq_extract(driver,logger):
    # print("💗TataCLiQ checkpoint 2 💗")
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CLASS_NAME, "PlpComponent__base"))
        )
        products = driver.find_elements(By.CLASS_NAME, "PlpComponent__base")
        products = products[:3]  #first 3 products
        results = []
        for i, product in enumerate(products):
            try:
                #image
                #image
                img_elem = product.find_element(By.CSS_SELECTOR, "img")
                image_url = img_elem.get_attribute("src")
                
                #product link
                product_link = product.find_element(By.CSS_SELECTOR, "a").get_attribute("href")                
                
                product_name=product.find_element(By.CLASS_NAME,"ProductDescription__boldText").text
                product_desc = product.find_element(By.CLASS_NAME, "ProductDescription__description").text
                product_price=product.find_element(By.CLASS_NAME, "ProductDescription__boldText").text
                
                product_data = {
                    "name": product_name,
                    "description": product_desc,
                    "price": product_price,
                    "image_url": image_url,
                    "product_link": product_link
                }
                
                results.append(product_data)
                logger.info(f"Extracted Tata CLiQ product {i+1}")
            except Exception as e:
                logger.error(f"Error extracting Tata CLiQ product: {e}")
                continue
        logger.info(f"Successfully extracted {len(results)} Tata CLiQ products")
        return results
    except Exception as e:
        logger.error(f"Error in tatacliq_extract: {e}")
        return []

# driver, results = setup_tatacliq_driver()
# print("🥰🥰🥰",results)

def executeTatacliqBase(text):
    #setting up logging
    output_folder = "Outputs\dress_type_images"
    logging.basicConfig(filename="bot_log.log", format="%(asctime)s - %(message)s", level=logging.DEBUG)
    logger = logging.getLogger()

    mini = text["price_range"]["min_range"]
    maxi = text["price_range"]["max_range"]
    gender = text["gender"]
    if gender=="F":
        gender_query="MSH10"
    else:
        gender_query="MSH11"
    _,results=setup_tatacliq_driver(text,output_folder,logger,gender_query,mini,maxi)
    return results
