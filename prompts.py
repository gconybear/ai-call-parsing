 
base ="""The following is a call between a customer and a call center agent at a self storage company called Red Dot Storage. The call is not broken up by speaker, you will have to infer who is speaking based on the content in the text. 

Your job is to decipher the text and produce the following fields in a JSON output: 

- `agent_name`: (str) the name of the agent, usually mentioned at the beginning of the call
- `sentiment`: (str) the sentiment of the customer. one of ["upset", "neutral", "happy"]
- `call_reason`: (str) the reason for the call 
- `customer_situation`: (str) a brief summary of the situation the customer is in or describing
- `agent_helpfulness`: (int) a rating of agent helpfulness on the scale of 1 (extremely unhelpful) to 5 (extremely helpful) 
- `agent_rating_explained`: (str) an explanation of how the call center agent performed in the call. feel free to be critical and suggest areas for improvement.
- `customer_name`: (str) customer name (first and last), this is usually prompted by the agent
- `customer_address`: (str) customer address, this is usually prompted by the agent 
- `customer_phone_number`: (str) customer phone number, this is usually prompted by the agent
- `customer_email_address`: (str) customer email address, this is usually prompted by the agent 

Your output should be a JSON object, nothing else, no words before or after. You ALWAYS answer in JSON.


Please produce a JSON response based on the following call transcript. 
"""  

whisper_prompt = "This is a call between a customer and a customer service agent for a self-storage company called Red Dot Storage"