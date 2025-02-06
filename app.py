from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import Form
from pydantic import BaseModel
import os
import openai
from typing import Annotated

class AskModel(BaseModel):
    question: str

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/greet/{name}")
def read_item(name: str):
    return {"Hello": name}

@app.post("/uploadfile/")
async def create_upload_file(request_string: Annotated[str, Form(...)], file: Annotated[UploadFile, File(...)]):
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    openai.api_key = OPENAI_API_KEY
    if OPENAI_API_KEY is None:
        raise HTTPException(status_code=500, detail="OpenAI API key is not set")
    
    try:
        contents = await file.read()
        print(request_string)
        # Construct context from the similar chunks' texts
        print(contents)
        #context_texts = [chunk for chunk in contents]
        #context = " ".join(context_texts)
        context = contents
        # Update the system message with the context
        system_message = f"You are a helpful assistant. Here is the context to use to reply to questions: {context}"

        # Make the OpenAI API call with the updated context
        response = openai.chat.completions.create(
             model="gpt-3.5-turbo",
             messages=[
                 {"role": "system", "content": system_message},
                 {"role": "user", "content": request_string},
             ]
         )
        print(system_message)
        return {"response": response.choices[0].message.content}
        #return {"response": "Kyon Ho Gaya na!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    #return {"filename": file.filename, "content": contents.decode()}