
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



from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

def scrape_first_3_reviews_flipkart(url):
    cService = ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    # Handle missing rating
    try:
        rating_elem = driver.find_element(By.CSS_SELECTOR, ".XQDdHH._6er70b")
        rating = rating_elem.text
    except NoSuchElementException:
        rating = "No rating available"

    # Try to fetch reviews
    try:
        wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="container"]/div/div[3]/div[1]/div[2]/div[6]/div[3]/div/div[1]')
        ))
        time.sleep(1)
        review_elements = driver.find_elements(By.CSS_SELECTOR, "div._11pzQk")
        review_texts = [elem.text for elem in review_elements[:3]]
        if not review_texts:
            review_texts = ["No reviews available"]
    except (NoSuchElementException, TimeoutException):
        review_texts = ["No reviews available"]

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })

    driver.quit()
    return reviews_data



def scrape_first_3_reviews_myntra(url):
    from selenium.common.exceptions import NoSuchElementException

    cService = webdriver.ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get(url)
    wait = WebDriverWait(driver, 20)

    reviews_data = []

    driver.execute_script("window.scrollTo(0, document.body.scrollHeight / 3);")
    time.sleep(2)

    # Try to extract rating
    try:
        rating_elem = driver.find_element(By.CLASS_NAME, "index-averageRating")
        rating = rating_elem.text
    except NoSuchElementException:
        rating = "no review available"

    # Try to extract reviews
    try:
        wait.until(EC.presence_of_element_located((By.XPATH, '//*[@id="mountRoot"]/div/div[1]/main/div[2]/div[2]/main/div/div')))
        time.sleep(1)
        review_elements = driver.find_elements(By.CLASS_NAME, "user-review-reviewTextWrapper")
        review_texts = [elem.text for elem in review_elements[:3]]
        if not review_texts:
            review_texts = ["no review available"]
    except Exception:
        review_texts = ["no review available"]

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })

    driver.quit()
    return reviews_data



def scrape_first_3_reviews_tatacliq(url):
    from selenium.common.exceptions import TimeoutException, NoSuchElementException

    cService = webdriver.ChromeService(executable_path=CHROMEDRIVER_PATH)
    driver = webdriver.Chrome(service=cService)
    driver.get(url)
    wait = WebDriverWait(driver, 20)
    
    reviews_data = []

    # Scroll down the page to load dynamic content
    for _ in range(3):
        driver.execute_script("window.scrollBy(0, window.innerHeight / 3);")
        time.sleep(1)

    try:
        # Try to get the overall rating
        rating_elem = wait.until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="root"]/div/div[3]/div/div[2]/div/div/div[2]/div[2]/div[1]/div[1]/div[1]'))
        )
        rating = rating_elem.text.strip() or "no rating available"
    except (TimeoutException, NoSuchElementException):
        rating = "no rating available"

    try:
        # Try to get reviews
        review_elements = driver.find_elements(By.CLASS_NAME, "ReviewPage__text")
        review_texts = [elem.text.strip() for elem in review_elements if elem.text.strip()]
        if not review_texts:
            review_texts = ["no review available"]
    except Exception:
        review_texts = ["no review available"]

    reviews_data.append({
        "url": url,
        "review": review_texts,
        "rating": rating
    })

    driver.quit()
    return reviews_data


    
def combine_all(scraped_data):
    grouped_reviews = {}

    print('\n\n\n REVIEW SCRAPED DATA', scraped_data)

    for platform, batches in scraped_data.items():
        print('PLATFORM', platform)
        platform_reviews = []

        for batch in batches:
            print('\n\n\n BATCH', batch)
            batch_reviews = []

            for item in batch:
                if not isinstance(item, list) or not item or not isinstance(item[0], dict):
                    print('Skipping invalid item:', item)
                    continue

                url = item[0].get("product_link")
                print('Extracted URL:', url)

                if not url:
                    continue

                if platform == "flipkart":
                    reviews = scrape_first_3_reviews_flipkart(url)
                elif platform == "myntra":
                    reviews = scrape_first_3_reviews_myntra(url)
                elif platform == "tata":
                    reviews = scrape_first_3_reviews_tatacliq(url)
                else:
                    reviews = []

                for review in reviews:
                    batch_reviews.append({
                        "url": url,
                        "review": review.get("review", []),
                        "rating": review.get("rating", "no rating available"),
                        "image_url" : item[0].get("image_url")
                        
                    })

            platform_reviews.append(batch_reviews)

        grouped_reviews[platform] = platform_reviews

    return grouped_reviews

         

if __name__=="__main__":
    
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
    ]
    # "nykaa" : [
    #     [
    #         "https://www.nykaafashion.com/it-girl-red-rose-dress/p/15137910"
    #     ],[
    #         "https://www.nykaafashion.com/ordinaree-floral-firecracker-printed-mini-dress/p/14271114"
    #     ]
    # ]
    # "tata" : [
    #     [
    #         "https://www.tatacliq.com/wardrobe-by-westside-burgundy-floral-lace-detailed-straight-dress/p-mp000000025695148"
    #     ],[
    #         "https://www.tatacliq.com/skylee-green-floral-kurta-with-pant-dupatta/p-mp000000023237217"
    #     ]
    # ]
    
}
    
    combine_all(urls_dict)




