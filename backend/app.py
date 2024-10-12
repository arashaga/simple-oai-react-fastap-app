from fastapi import FastAPI, Request, HTTPException
import os
import logging
from openai import AzureOpenAI
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# Logging Configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Azure OpenAI Client Setup
endpoint = os.getenv("ENDPOINT_URL", "https://gpt4-assistants-api.openai.azure.com/")
deployment = os.getenv("DEPLOYMENT_NAME", "gpt-35-turbo")
subscription_key = os.getenv("AZURE_OPENAI_API_KEY", "REPLACE_WITH_YOUR_KEY_VALUE_HERE")

client = AzureOpenAI(
    azure_endpoint=endpoint,
    api_key=subscription_key,
    api_version="2024-05-01-preview",
)

# Add CORS middleware to allow frontend to communicate with backend
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change "*" to specific origins if needed for security
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

@app.post("/chat")
async def chat(request: Request):
    try:
        # Log incoming request data
        logger.info("Received request at /chat endpoint")
        body = await request.json()
        user_message = body.get("message")
        if not user_message:
            raise HTTPException(status_code=400, detail="Message not provided")

        # Log before calling Azure OpenAI API
        logger.info(f"Sending request to Azure OpenAI API: {user_message}")
        response = client.chat.completions.create(
            model=deployment,
            messages=[
                {
                    "role": "system",
                    "content": "You are an AI assistant that helps people find information."
                },
                {
                    "role": "user",
                    "content": user_message
                }
            ],
            max_tokens=800,
            temperature=0.7,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None,
            stream=False
        )

        # Log response from Azure OpenAI API
        logger.info(f"Received response from Azure OpenAI API: {response}")

        # Extract the response content properly
        message_content = response.choices[0].message.content.strip()
        return {"response": message_content}

    except Exception as e:
        logger.error(f"Error processing request: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal Server Error")
