from .baseAgent import baseAgent

class orchestrator2Agent(baseAgent):
    
    def __init__(self):
        super().__init__(name="secondHalf", instructions="""
                         
                         
                         
                         
                         """)
        
    async def run(self,messages : list):
        
        print(messages,'MESSAGES SECOND')
        
        
        return {
            "messages" : messages
        }
    
    