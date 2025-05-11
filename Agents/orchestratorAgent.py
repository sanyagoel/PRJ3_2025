from .baseAgent import baseAgent
from .dressTypeAgent import dressType
from .scraperAgent import scraperAgent

class orchestratorAgent(baseAgent):
    
    def __init__(self):
        super().__init__(name="orchestrator", instructions="""
                         
                         
                         
                         
                         """)
        
        self.dressType = dressType()
        self.scraper = scraperAgent()
        
    async def run(self,messages:list):
        
        # print('MESSAGES',messages)
        
        dress_types = await self.dressType.run(messages)
        
        # print('DRESS TYPES',dress_types)
        
        scraped_content = await self.scraper.run([{
            "role" :"user",
            "content" : dress_types
        }])
        
        print('SCRAPED CONTENT', scraped_content)
        
        
        return {
            "messages" : messages,
            "dresstypes" : dress_types,
            "scraped_content" : scraped_content
        }
        
        
        
        