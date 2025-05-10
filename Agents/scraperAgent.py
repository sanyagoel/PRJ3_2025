from .baseAgent import baseAgent


class scraperAgent(baseAgent):
    
    def __init__(self):
        super().__init__(name="scraper", instructions="""
                         
                         
                         
                         """)
        
        
    async def run(self,messages : list):
        
        content = messages[-1].get("content")
        
        
            
        
        