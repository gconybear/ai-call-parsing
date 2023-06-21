import openai 
import os 
from dotenv import load_dotenv  
import numpy as np


# Load environment variables from .env file
load_dotenv() 

API_KEY = os.getenv('OPENAI_API_KEY')

class ai: 
    
    def __init__(self, index, key=API_KEY, system_prompt=''): 
        
        # pinecone index for vector retrieval 
        self.index = index 
        openai.api_key = API_KEY  

        if system_prompt != '':  
            self.sys_mssg = [{"role": "system", "content": system_prompt}] 
        else: 
            self.sys_mssg = []


    def embed(self, text):  

        EMBEDDING_MODEL = "text-embedding-ada-002"
        
        result = openai.Embedding.create(
          model=EMBEDDING_MODEL,
          input=text
        )
        return result["data"][0]["embedding"] 
    
    def nearest_docs(self, V: list[float], K=10):  
        
        "finds the nearest docs given an embedding"
        
        return self.index.query([V], top_k=K, include_metadata=True) 
    
    def embed_and_get_closest_docs(self, Q: str): 
        """
        embeds a query Q and does a vector search for most similar documents
        """ 

        v = self.embed(Q) 
        docs = self.nearest_docs(v)  
        
        return docs.to_dict() 


    def construct_prompt(self, head): 
        return head 

    def answer(self, Q, preprompt='', history=[], model='gpt-3.5-turbo-0613', temperature=0.5):   

        full_hist = self.sys_mssg + history + [{"role": "user", "content": Q}]

        #full_hist = self.sys_mssg + history + [{"role": "user", "content": preprompt + prompt}]  # oldest to newest

        response = openai.ChatCompletion.create(
                    model=model, 
                    messages=full_hist, 
                    temperature=temperature,
                    )  
        
        self.chat_log = full_hist 

        #self.chat_log.append({"role": "assistant", "content": response['choices'][0]['message']['content']})

        return response['choices'][0]['message']['content']

        

