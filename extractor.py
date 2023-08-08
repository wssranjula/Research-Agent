import openai
import os
from dotenv import load_dotenv
from fastapi import FastAPI
from pydantic import BaseModel

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

app = FastAPI()

function_descriptions = [
    {
        "name": "extract_info_from_email",
        "description": "categorise & extract key info from an email, such as use case, company name, contact details, etc.",
        "parameters": {
            "type": "object",
            "properties": {
                "Property_id": {
                    "type": "string",
                    "description": "ID number of the property"
                },
                "Property_address": {
                    "type": "string",
                    "description": " address of the property"
                },
                "Property_url": {
                    "type": "string",
                    "description": "url of the property"
                },
                "Name": {
                    "type": "string",
                    "description": "the name of the  client"
                },                                        
                "Email": {
                    "type": "string",
                    "description": "Email address of the user"
                },
                "Phone":{
                    "type": "string",
                    "description": "phone number of the client"
                },
                "Category": {
                    "type": "string",
                    "description": "Try to categorise this email into categories like those: 1. Sales 2. customer support; 3. consulting; 4. partnership; etc."
                },
                "about_client":{
                    "type": "string",
                    "description": "short description about client"
                },
                "priority": {
                    "type": "string",
                    "description": "Try to give a priority score to this email based on how likely this email will leads to a good business opportunity, from 0 to 10; 10 most important"
                },
            },
            "required": ["Property_id","Property_address","Property_url","Name", "Email", "Phone", "priority", "Category"]
        }
    }
]


# email = """
# Hi Ebony Murray,

# you have received a new lead from realestate.com.au

# Property ID : 12334566
# property address : address availble on request windaro Qid 147
# Property URL : www.jhondoe.com/test/124


# User Details

# here are the information about the user.
# Name : Donald Trump
# Email :donald@gmail.com
# Phone : 94123312312
# About me : Polician with 10n years of experince
# I would like to : Looking to buy an aprtment.
# Thanks


# """

# prompt = f"Please extract Only User Details from this email: {email} "
# message = [{"role": "user", "content": prompt}]

# response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo-0613",
#     messages=message,
#     functions = function_descriptions,
#     function_call="auto"
# )

# print(response)



class Email(BaseModel):
    from_email: str
    content: str

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/")
def analyse_email(email: Email):
    content = email.content
    query = f"Please extract key user information from this email: {content} . if you cant find the information, please specify none. "

    messages = [{"role": "user", "content": query}]

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-0613",
        messages=messages,
        functions = function_descriptions,
        function_call="auto"
    )

    arguments = response.choices[0]["message"]["function_call"]["arguments"]
    Property_id =eval(arguments).get('Property_id')
    Property_address = eval(arguments).get('Property_address')
    Property_url = eval(arguments).get('Property_url')
    Name = eval(arguments).get("Name")
    priority = eval(arguments).get("priority")
    Phone = eval(arguments).get("Phone")
    Email = eval(arguments).get("Email")
    category = eval(arguments).get("category")
    # nextStep = eval(arguments).get("nextStep")

    return {
        "Property_id": Property_id,
        "Property_address": Property_address,
        "Property_url": Property_url,
        "Name": Name,
        "Phone": Phone,
        "Email": Email,
        "priority": priority,
        "category": category
        
    }