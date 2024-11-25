from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import subprocess
import requests
from dotenv import load_dotenv
import os

load_dotenv()
LLAMA_API_KEY = os.getenv("LLAMA_API_KEY")

app = FastAPI()

class QueryModel(BaseModel):
    query: str

# Replace with actual API keys and endpoints for travel services
FLIGHT_API_URL = "https://api.skyscanner.net/apiservices/"
HOTEL_API_URL = "https://api.booking.com/"
TRANSPORT_API_URL = "https://api.transportdata.com/"
LLAMA_API_URL = "https://www.llama-api.com/"
LLAMA_API_KEY = LLAMA_API_KEY

def llama_integration(user_query: str):
    """
    Integrate with the Llama API to process the user's query.
    """
    try:
        headers = {
            "Authorization": f"Bearer {LLAMA_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {"query": user_query}
        
        response = requests.post(LLAMA_API_URL, json=payload, headers=headers)
        response.raise_for_status()
        return response.json().get("response", "No response received from Llama.")
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Llama API error: {str(e)}")
    

def fetch_travel_data(destination: str):
    try:
        # Fetch flight options
        flights = requests.get(f"{FLIGHT_API_URL}/search", params={"destination": destination}).json()

        # Fetch accommodations
        accommodations = requests.get(f"{HOTEL_API_URL}/search", params={"destination": destination}).json()

        # Fetch transport options
        transport = requests.get(f"{TRANSPORT_API_URL}/search", params={"destination": destination}).json()

        return {
            "flights": flights,
            "accommodations": accommodations,
            "transport": transport
        }
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error fetching travel data: {str(e)}")

@app.post("/api/chat")
async def chat_with_ai(query: QueryModel):
    # Process the user query with Llama
    processed_query = llama_integration(query.query)

    # Assume the Llama response includes the destination
    destination = processed_query.split("Destination: ")[-1].strip()
    travel_data = fetch_travel_data(destination)

    return {
        "processed_query": processed_query,
        "travel_data": travel_data
    }
