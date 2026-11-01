import os
from time import sleep
from pathlib import Path
from dotenv import load_dotenv
from groq import Groq
from pydantic import BaseModel, Field
import json
# from compare_resume import compare_resume
# from myinfo import Resume

load_dotenv()
my_api_key=os.getenv("GROQ_API_KEY")

if not my_api_key:
    raise ValueError("API key kaha hai bhai")

client=Groq(api_key=my_api_key)
model="openai/gpt-oss-120b"

class Experience(BaseModel):
    company: str | None = None
    role: str | None = None
    duration: str | None = None
    description: str | None = None
    skills_used: list[str] = []

class Resume(BaseModel):
    name: str | None = None
    email: str | None = None
    phone: str | None = None

    total_experience_years: float | None = None

    skills: list[str] = []
    experiences: list[Experience] = []
    education: list[str] = []
    projects: list[str] = []
    certifications: list[str] = []

with open("profile.json", "r") as f:
    data = json.load(f)
profile = Resume(**data)


system_prompt = f"""

You are my professional assistant.

Here is infromation about me:
{profile.model_dump_json(indent=4)}

You have to answer questions exactly based on this profile.
Do not invent new information.
Do not lie , be honest in the conversation.
Do not sugarcoat things about me.
If you dont know the answer simply return "i don't know".



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

Do not overexplain things , give your reply to the point about my information.


"""

messages = [
    {
        "role": "system",
        "content": system_prompt
    }
]



    




while True:

    user_input = input("enter your query:")

    if user_input == "exit":
        break

    # if user_input.lower() == "compare":
    #     pdf_name = input("Enter pdf name: eg(amazon.pdf)")
    #     pdf_path = Path("job_desc_files")/pdf_name
    #     report = compare_resume(profile,pdf_path)
    #     print(report)
    #     continue


    messages.append({
        "role":"user",
        "content":user_input
    })

    response = client.chat.completions.create(model=model,messages=messages)

    answer = response.choices[0].message.content
    print("ChatBot:", answer)

    messages.append({
        "role":"assistant",
        "content":answer
    })



