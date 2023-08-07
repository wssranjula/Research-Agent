import requests

print(requests.post(
    "http://localhost:10000",
    json={"from_email": "realestate@gmail.com.au",
          "content": """
# Hi Ebony Murray,
Hope you are doing good
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
          }
).json()
)