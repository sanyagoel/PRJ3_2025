
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

#_11pzQk

#https://www.flipkart.com/search?q=red+dress

# {
    
#     "myntra" : [
#         [
#             "jeans url",
#             "top url"
#         ],
#         [
#             "skirt url",
#             "jacket url"
#         ]
#     ],
    
#     "flipkart" : [
#         [
            
#         ]
#     ],
#     "savana" : [
        
#     ]
    
# }

CHROMEDRIVER_PATH = r"C:\Users\Admin\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe"

urls_dict = {
    "flipkart": [
        [
            "https://www.flipkart.com/alekya-women-bodycon-red-midi-calf-length-dress/p/itm518d50917c7fd?pid=DREGCF4DUP7G2FEP&lid=LSTDREGCF4DUP7G2FEP92VB7N&marketplace=FLIPKART&q=red+dress&store=clo%2Fodx%2Fmaj&srno=s_1_4&otracker=search&otracker1=search&fm=Search&iid=09c0e233-79a9-4bd8-84c0-e3fe4e432827.DREGCF4DUP7G2FEP.SEARCH&ppt=sp&ppn=sp&ssid=0v9qo258ao0000001746980330463&qH=9fc22438e26fbca8",
            "https://www.flipkart.com/roadster-women-a-line-red-ankle-length-dress/p/itm6fa2c79ce1c80?pid=DREH4DCXRQHADNCZ&lid=LSTDREH4DCXRQHADNCZTIRY1J&marketplace=FLIPKART&q=red+dress&store=clo%2Fodx%2Fmaj&srno=s_1_1&otracker=search&otracker1=search&fm=organic&iid=en_LjXzHYi2JBJCdncHN0vCh2FyN015KEwGyB_bSWjev0Z56VusSBC2uRW-R6lk7M8bAPt-CHE2bvmfJwhHGEd2Cw%3D%3D&ppt=hp&ppn=homepage&ssid=1q3jwu0buo0000001746980238787&qH=9fc22438e26fbca8"
        ]
    ],
    
    "myntra" : [
        [
            "https://www.myntra.com/dresses/neudis/neudis-red-satin-dress/16461648/buy"
        ],[
            "https://www.myntra.com/dresses/tokyo+talkies/tokyo-talkies-red-sheath-dress/18954164/buy",
            "https://www.myntra.com/dresses/athena/athena-women-red-sheath-dress/10322627/buy"
        ]
    ],
    # "nykaa" : [
    #     [
    #         "https://www.nykaafashion.com/it-girl-red-rose-dress/p/15137910"
    #     ],[
    #         "https://www.nykaafashion.com/ordinaree-floral-firecracker-printed-mini-dress/p/14271114"
    #     ]
    # ]
    "tata" : [
        [
            "https://www.tatacliq.com/wardrobe-by-westside-burgundy-floral-lace-detailed-straight-dress/p-mp000000025695148"
        ],[
            "https://www.tatacliq.com/skylee-green-floral-kurta-with-pant-dupatta/p-mp000000023237217"
        ]
    ]
    
}

def scrape_first_3_reviews_flipkart(url):
    
    cService = webdriver.ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    
    rating_elem = driver.find_element(By.CSS_SELECTOR, ".XQDdHH._6er70b")
    rating = rating_elem.text
    
        
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[6]/div[3]/div/div[1]')))
    time.sleep(1) 

        
    review_elements = driver.find_elements(By.CSS_SELECTOR, "div._11pzQk")
    review_texts = [elem.text for elem in review_elements[:3]]



    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })
    driver.quit()
    return reviews_data


def scrape_first_3_reviews_myntra(url):
    
    cService = webdriver.ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    
    rating_elem = driver.find_element(By.CLASS_NAME, "index-averageRating")
    rating = rating_elem.text
        
        
    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mountRoot"]/div/div[1]/main/div[2]/div[2]/main/div/div')))
    time.sleep(1) 

        
    review_elements = driver.find_elements(By.CLASS_NAME, "user-review-reviewTextWrapper")
    review_texts = [elem.text for elem in review_elements[:3]]

 

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })
    driver.quit()
    return reviews_data


def scrape_first_3_reviews_tatacliq(url):
    
    cService = webdriver.ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    
    for _ in range(8):
        driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")
        time.sleep(1)

    wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]')))

    # rating_elem = driver.find_element(By.CLASS_NAME, "RatingAndIconComponent__ratingText")
    
    rating_elem = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]'))
    )
    rating = rating_elem.text

    time.sleep(2)    
    # wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]')))
    # time.sleep(1) 



    review_elements = driver.find_elements(By.CLASS_NAME, "ReviewPage__text")
    review_texts = [elem.text for elem in review_elements]


    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })
    driver.quit()
    return reviews_data
    

    
def combine_all(urls_dict):
    flipkart_reviews = []

    for group in urls_dict["flipkart"]:
        group_reviews = []
        
        for url in group:
            print(f"SCRAPED URL {url}")
            reviews = scrape_first_3_reviews_flipkart(url)
            
            group_reviews.append(reviews)
        flipkart_reviews.append(group_reviews)
        
    myntra_reviews = []

    for group in urls_dict["myntra"]:
        group_reviews = []
        
        for url in group:
            print(f"SCRAPED URL {url}")
            reviews = scrape_first_3_reviews_myntra(url)
            
            group_reviews.append(reviews)
        myntra_reviews.append(group_reviews)
        
        
    tata_reviews = []

    for group in urls_dict["tata"]:
        group_reviews = []
        
        for url in group:
            print(f"SCRAPED URL {url}")
            reviews = scrape_first_3_reviews_tatacliq(url)
            
            group_reviews.append(reviews)
        tata_reviews.append(group_reviews)
    
    return {
            
    "flipkart": flipkart_reviews, 
            
    "myntra" : myntra_reviews,
    
    "tata" : tata_reviews
    }
         


result = combine_all(urls_dict)

print(result)




