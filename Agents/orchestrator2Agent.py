from .baseAgent import baseAgent
from .multiScraperAgent import multiScraperAgent
from WebScraping.reviewScraper import combine_all

class orchestrator2Agent(baseAgent):
    
    def __init__(self):
        super().__init__(name="secondPhase", instructions="""                   
                         """)
        self.multi_scraper = multiScraperAgent()
        
    async def run(self,messages : list):
        
        
        # min_range = content["price_range"][0]
        # max_range = content["price_range"][1]
        # gender = content["gender"]
        # selected_list = content["selected_dresses"]

        print('🎀🎀MESSAGES new o2',messages)
        scraped1 = await self.multi_scraper.run(messages)
        print('SCRAPED--=CONTENT', scraped1)
        
        result2 = combine_all(scraped1)
        print('\n\n\n\n RESULT 2',result2)
    
        return {
            "messages" : result2,
        }