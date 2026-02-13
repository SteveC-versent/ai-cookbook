import os

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel

load_dotenv("../.env")

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# --------------------------------------------------------------
# Step 1: Define the response format in a Pydantic model
# --------------------------------------------------------------


class CalendarEvent(BaseModel):
    name: str
    date: str
    participants: list[str]


# --------------------------------------------------------------
# Step 2: Call the model
# --------------------------------------------------------------

completion = client.chat.completions.parse(
    model="gpt-5-mini",
    messages=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    response_format=CalendarEvent,
)

# --------------------------------------------------------------
# Step 3: Parse the response
# --------------------------------------------------------------

event = completion.choices[0].message.parsed
print(f"Event Name: {event.name}")
print(f"Event Date: {event.date}")
print(f"Event Participants: {', '.join(event.participants)}")


# --------------------------------------------------------------
# Alternative implementation using client.responses.parse
# --------------------------------------------------------------

response = client.responses.parse(
    model="gpt-4o-2024-08-06",
    input=[
        {"role": "system", "content": "Extract the event information."},
        {
            "role": "user",
            "content": "Alice and Bob are going to a science fair on Friday.",
        },
    ],
    text_format=CalendarEvent,
)

response_event = response.output_parsed
print(f"Event Name: {response_event.name}")
print(f"Event Date: {response_event.date}")
print(f"Event Participants: {', '.join(response_event.participants)}")
