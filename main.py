from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Initialize GenAI API
genai.configure(api_key='AIzaSyBLdPt9xCo9Ia1vpBuxfCl9EMq0FqXByyI')
generation_config = {
  "temperature": 1,
  "top_p": 0.95,
  "top_k": 0,
  "max_output_tokens": 8192,
  "response_mime_type": "application/json",
}
# model_json = genai.GenerativeModel('gemini-1.5-pro-latest' ,
#                               generation_config=generation_config)
model = genai.GenerativeModel('gemini-1.5-pro-latest')
# chat = model.start_chat(history=[])


models = dict()

# Define a data model for the request body
class Query(BaseModel):
    query: str
    session_id : int
    


# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for generating responses
@app.get("/generate/")
async def generate_response(query: str , session_id: int):
    global models
    if session_id not in models :
        models[session_id] = model.start_chat(history=[])
    
    try :
        # response = model.generate_content(query)
        
        response = models[session_id].send_message(query)

        return {"response": response.text , "Prompt" :  query}
    except Exception as e:
        return {"error": str(e)}
    

@app.get("/")
async def read_root():
    return {"message": "Hello To Gemini Pro API"}

@app.get("/remove/")
async def remove_session(session_id: int):
    if session_id in models :
        del models[session_id]
        return {"message": f"{session_id} - session  suspended successfully"}
    else :
        return {"message": f"{session_id} - session not found"}


# Run the server with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Server running on port 8000")