from .baseAgent import baseAgent
from .dressTypeAgent import dressType

class orchestratorAgent(baseAgent):
    
    def __init__(self):
        super().__init__(name="orchestrator", instructions="""
                         
                         
                         
                         
                         """)
        
        self.dressType = dressType()
        
    async def run(self,messages:list):
        
        print('MESSAGES',messages)
        
        dress_types = await self.dressType.run(messages)
        
        
        return {
            "messages" : messages,
            "dresstypes" : dress_types,
        }
        
        
        
        