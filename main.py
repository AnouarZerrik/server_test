from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai

# Initialize GenAI API
genai.configure(api_key='AIzaSyBLdPt9xCo9Ia1vpBuxfCl9EMq0FqXByyI')
model = genai.GenerativeModel('gemini-pro')

# Define a data model for the request body
class Query(BaseModel):
    query: str

# Create an instance of the FastAPI class
app = FastAPI()

# Define a route for generating responses
@app.get("/generate/")
async def generate_response(query: str):
    try :
        response = model.generate_content(query)
        return {"response": response.text , "Prompt" :  query}
    except Exception as e:
        return {"error": str(e)}
    

# Run the server with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    print("Server running on port 8000")