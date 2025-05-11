from .baseAgent import baseAgent
import ast

from Scraper.baseScraper import executeBase

class scraperAgent(baseAgent):
    
    def __init__(self):
        super().__init__(name="scraper", instructions="""
                         
                 
                 
                         
                         
                         """)
        
        
    async def run(self,messages : list):
        
        content = messages[-1].get("content")
        
        min_range = content["min_range"]
        
        max_range = content["max_range"]
        
        gender = content["gender"]
        
        dress_types_list = ast.literal_eval(content["result"][0]["content"])
        # print('EXTRACT?',content)
        
        print(min_range,'min_range')
        
        print(gender, 'GENDER')
        
        print(dress_types_list,'dress_types_listtt')
        
    #       for i in text["dress types"]:
    #     dress_query.append(i)
    #     # print(i)

    # if text["gender"]=="F":
    #     gender_query="f=Gender%3Amen%20women%2Cwomen"
    # else:
    #     gender_query="f=Gender%3Aboys%2Cboys%20girls"
        
    # mini=text["price range"]["min_range"]
    # maxi=text["price range"]["max_range"]
    
        text = {
            "dress types" : dress_types_list,
            "price range" : {
                "min_range" : min_range,
                "max_range" : max_range
            },
            "gender" : gender
        }
        
        dressResults = executeBase(text)
        
        # print('DRESS RESULTS',dressResults)
        
        
        
        return {
            "dressResults" : dressResults,
            "dress_types" : dress_types_list,
            "gender" : gender,
             "price range" : {
                "min_range" : min_range,
                "max_range" : max_range
            }
        }
        
        

        
        