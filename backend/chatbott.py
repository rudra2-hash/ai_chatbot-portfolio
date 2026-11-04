import os
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
import json

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
# from compare_resume import compare_resume
# from myinfo import Resume

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

# class Experience(BaseModel):
#     company: str | None = None
#     role: str | None = None
#     duration: str | None = None
#     description: str | None = None
#     skills_used: list[str] = []

# class Resume(BaseModel):
#     name: str | None = None
#     email: str | None = None
#     phone: str | None = None

#     total_experience_years: float | None = None

#     skills: list[str] = []
#     experiences: list[Experience] = []
#     education: list[str] = []
#     projects: list[str] = []
#     certifications: list[str] = []

with open("profile.json", "r") as f:
    profile = json.load(f)

profile_context = json.dumps(profile, indent=4)



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.api_route("/health", methods=["GET", "HEAD"])
def health():
    return {"status": "ok"}

sessions = {}




#creating system prompt and fitting it once instead of appending each time


system_prompt = f"""

You are my professional assistant.

Your tone should be polite and frinedly. 

Here is infromation about me:
{profile_context}

You have to answer questions exactly based on this profile.
Do not invent new information.
Do not lie , be honest in the conversation.
Do not sugarcoat things about me.
If you dont know the answer simply return "i don't know".

Simple questions like "whats your name"? should not be ignored by you. You have to answer even small answers based on my information.

Asnwer the questions briefly according to the profile.

Only answer the questions basedon professional information required for job purpose.
Only continue the conversation if recuriter is for IT or Computer field.

For eg:
user : 'I have sales company , i need salesman'?
your reply : 'not my role'

If the user ask personal questions or irrelavant questions, return "out of context".
For eg: 
user : 'tell me about your girlfriend?
your reply : 'out of context'

When the user asks for links like "whast your github link" , you should give that link without any story. DO NOT invent links

The user can  chat about my projects , when user chats about my projects answer only on the skills or stack i have worked actually.

If the suer asks for my project link give the link , if any project is live and user asks for live link than give that live link or github link accordingly


Do not overexplain things , give your reply to the point about my information.


"""

 


class Info(BaseModel):
    query:str
    session_key:str
    # session_id:str
   

@app.post("/hello")
def hello(info:Info):

    user_input = info.query
    session_id = info.session_key

    if session_id not in sessions:
        sessions[session_id] = [ 
            {"role":"system","content":system_prompt}
        ]

    messages = sessions[session_id]

    messages.append({
        "role": "user",
        "content": user_input
    }) 


    response = client.chat.completions.create(model=model,messages=messages)

    answer = response.choices[0].message.content
    

    messages.append({
        "role":"assistant",
        "content":answer
    })

    return {"answer":answer}

   
    