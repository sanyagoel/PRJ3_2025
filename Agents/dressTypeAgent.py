from .baseAgent import baseAgent

class dressType(baseAgent):
    
    def __init__(self):
        super().__init__(name="dressType", instructions="""
                         
                         You are a fashion advisor. Given details about an event, the user's gender, suggest exactly 5
                         different specific dress types that would be suitable. Each suggestion must be concrete and descriptive, including color, 
                         style, and any notable details (for example: "a blue medium-length dress with lace in between, perfect for a house party"). 
                         Always base your suggestions primarily on the event type and gender.
                        Format your response as a numbered list of exactly 5 detailed dress suggestions.
                         
                         
                         """)
        
        
    async def run(self,messages:list):
            
            content = messages[-1].get("content")
            
            prompt  =  f"""
Given the following information:
- Event type: {content.get("event_type")}
- Gender: {content.get("gender")}

Return exactly 5 suitable dress types as a Python list of strings. 
Each string should be a specific dress type, e.g., "Blue lace midi dress" or "Embroidered Anarkali suit". 
Do NOT include any explanation, numbering, or extra text-only output a valid Python list of 5 dress type strings.
    """
            
            result = self.query_ollama(prompt)
            
            return {
                "result":result,
                "min_range" : content.get("price_range")[0],
                "max_range" : content.get("price_range")[1]
            }