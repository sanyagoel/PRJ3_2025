from .baseAgent import baseAgent

class dressType(baseAgent):
    
    def __init__(self):
        super().__init__(name="dressType", instructions="""
                         
                         You are a fashion advisor. Given details about an event and the user's gender, suggest exactly 5 different specific dress types that would be suitable.
Each suggestion must be concrete and descriptive, including color, style, and any notable details (for example: "blue lace midi dress").
Always base your suggestions primarily on the event type and gender. Keep the dress types simple and easy to find.
Format your response as a Python list of exactly 5 lists. Each inner list must contain the clothing items that together make up one dress type.
Always use a list for each dress type, even for single-piece dresses (e.g., ["blue lace midi dress"]).
Do NOT include any explanation, numbering, or extra text-only output the Python list. **Do not include any accessories at all.**
Also make sure u do NOT use very complex words so that I can find these dresses online easily.

                         
                         """)
        
        
    async def run(self,messages:list):
            
            content = messages[-1].get("content")
            
            prompt = f"""
Given the following information:
- Event type: {content.get("event_type")}
- Gender: {content.get("gender")}

Return exactly 5 suitable dress types as a Python list of lists.
Each inner list must contain the clothing items that together make up one dress type.
- If a dress type consists of multiple items (e.g., "top and jeans"), split them into separate strings within the list: ["top", "jeans"].
- For single-piece dresses, use a one-item list with the dress name as the only string, e.g., ["floral green dress"].

Your response MUST be a valid Python list of 5 lists, starting with [ and ending with ].
Here is the exact format you MUST follow:

[
    ["black off-the-shoulder top", "flowy white skirt"],
    ["floral green dress"],
    ["sunglasses", "brown ankle-strap sandals"],
    ["navy blue cardigan", "white tank top"],
    ["khaki culottes", "pastel pink top"]
]

Replace the example items above with your actual suggestions. Do NOT include any explanation, numbering, extra text, or comments-only output the Python list of 5 lists as shown.
Also make sure u do NOT use very complex words so that I can find these dresses online easily.
"""


            gender = content.get("gender")[0].upper()
            
            result = self.query_ollama(prompt)
            
            return {
                "result":result,
                "min_range" : content.get("price_range")[0],
                "max_range" : content.get("price_range")[1],
                "gender" : gender
            }