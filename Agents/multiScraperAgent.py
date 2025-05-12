from .baseAgent import baseAgent
import ast
from WebScraping.myntraScraper import executeMyntraBase
from WebScraping.flipkartScraper import executeFlipkartBase

class multiScraperAgent(baseAgent):
    def __init__(self):
        super().__init__(name="multi_craper", instructions="""                                
                         """)
 
    async def run(self,messages : list):
        content = messages[-1]["content"]
        print("💗 rcd msgs: ",messages)
        min_range = content["price_range"]["min_range"]
        max_range = content["price_range"]["max_range"]
        gender = content["gender"]
        selected_list = content["selected_dresses"]
        
        text = {
            "dress_types": selected_list,
            "price_range": {
                "min_range": min_range,
                "max_range": max_range
            },
            "gender": gender
        }
        print("💗formed text: ",text)
        flipkart_results=executeFlipkartBase(text)
        myntra_results=executeMyntraBase(text)
        
        print('🛍️MYNTRA. RESULTS',myntra_results)
        print('FLIPKART. RESULTS',flipkart_results)
        
        return({
            "myntra" : myntra_results,
            "flipkart" : flipkart_results
        })
        # return {
        #     "dress_types" : selected_list,
        #     "gender" : gender,
        #     "min_range" : min_range,
        #     "max_range" : max_range
        # }
        
        

        
        