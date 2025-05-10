from openai import OpenAI
from swarm import Agent,Swarm

class baseAgent():
   
    def __init__(self, name : str, instructions : str):
       self.name = name
       self.instructions = instructions
       self.ollamaClient = OpenAI(base_url='http://localhost:11434/v1',api_key = 'ollama')
       self.swarm = Agent(name=name, instructions = instructions, model='llama3.2:latest')
       self.client = Swarm(client = self.ollamaClient)
      
       
    async def run(self,messages : list):
        raise NotImplementedError('This method needs to be implemented..')
    
    def query_ollama(self,prompt : str):
        
        response = self.client.run(agent=self.swarm, messages=[{
            "role" : "user",
            "content" : prompt
        }])
        
        return response.messages
    
    
        
    
    
    
       

