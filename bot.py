import os
import json
import asyncio
import logging
from typing import Dict, Any
from fastapi import FastAPI, WebSocket
from openai import OpenAI
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Check for required environment variables
if not os.getenv("OPENAI_API_KEY"):
    raise ValueError("OPENAI_API_KEY environment variable is not set")

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Store active conversations
active_conversations: Dict[str, Any] = {}

def make_search(json_data: str) -> str:
    """
    Function to handle search requests
    """
    try:
        # Parse the JSON data
        search_data = json.loads(json_data)
        logger.info(f"Received search request with data: {search_data}")
        
        # Here you can implement your search logic
        # For now, we'll just return a mock response
        return json.dumps({
            "status": "success",
            "message": "Search completed",
            "data": search_data
        })
    except json.JSONDecodeError:
        return json.dumps({
            "status": "error",
            "message": "Invalid JSON format"
        })
    except Exception as e:
        return json.dumps({
            "status": "error",
            "message": str(e)
        })

def get_or_create_assistant():
    """
    Get the assistant ID from environment or create a new assistant
    """
    assistant_id = os.getenv("ASSISTANT_ID")
    
    if assistant_id:
        try:
            # Try to retrieve the existing assistant
            assistant = client.beta.assistants.retrieve(assistant_id)
            logger.info(f"Found existing assistant: {assistant.name}")
            return assistant_id
        except Exception as e:
            logger.warning(f"Could not find assistant with ID {assistant_id}: {str(e)}")
    
    # Create a new assistant
    logger.info("Creating new assistant")
    assistant = client.beta.assistants.create(
        name="AI Chat Assistant",
        instructions="""You are a helpful AI assistant that can help users with their questions and tasks.
        When a user asks for a search, use the makeSearch function with the appropriate JSON data.
        The JSON should contain the search parameters in a structured format.""",
        model="gpt-4-turbo-preview",
        tools=[{
            "type": "function",
            "function": {
                "name": "makeSearch",
                "description": "Perform a search operation with the given JSON parameters",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "json": {
                            "type": "string",
                            "description": "JSON string containing search parameters"
                        }
                    },
                    "required": ["json"]
                }
            }
        }]
    )
    
    # Save the new assistant ID to .env file
    with open('.env', 'a') as f:
        f.write(f"\nASSISTANT_ID={assistant.id}")
    
    logger.info(f"Created new assistant with ID: {assistant.id}")
    return assistant.id

# Get or create assistant at startup
ASSISTANT_ID = get_or_create_assistant()

async def process_message_with_assistant(message: str, conversation_id: str) -> str:
    """
    Process a message using the OpenAI assistant and return the response.
    """
    try:
        logger.info(f"Processing message for conversation {conversation_id}")
        
        # Get or create conversation thread
        if conversation_id not in active_conversations:
            logger.info("Creating new thread")
            thread = client.beta.threads.create()
            active_conversations[conversation_id] = thread.id
        else:
            logger.info("Retrieving existing thread")
            thread_id = active_conversations[conversation_id]
            thread = client.beta.threads.retrieve(thread_id)

        # Add message to thread
        logger.info("Adding message to thread")
        client.beta.threads.messages.create(
            thread_id=thread.id,
            role="user",
            content=message
        )

        # Run the assistant
        logger.info("Running assistant")
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=ASSISTANT_ID
        )

        # Wait for the run to complete
        while True:
            run_status = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            
            logger.info(f"Run status: {run_status.status}")
            
            if run_status.status == 'completed':
                break
            elif run_status.status == 'failed':
                logger.error(f"Run failed: {run_status.last_error}")
                return f"Sorry, I encountered an error: {run_status.last_error}"
            elif run_status.status == 'expired':
                logger.error("Run expired")
                return "Sorry, the request timed out. Please try again."
            elif run_status.status == 'requires_action':
                # Handle function calls
                for tool_call in run_status.required_action.submit_tool_outputs.tool_calls:
                    if tool_call.function.name == "makeSearch":
                        # Get the JSON parameter
                        args = json.loads(tool_call.function.arguments)
                        json_data = args.get("json", "{}")
                        
                        # Call the function
                        result = make_search(json_data)
                        
                        # Submit the result back to the assistant
                        client.beta.threads.runs.submit_tool_outputs(
                            thread_id=thread.id,
                            run_id=run.id,
                            tool_outputs=[{
                                "tool_call_id": tool_call.id,
                                "output": result
                            }]
                        )
            
            await asyncio.sleep(1)

        # Get the assistant's response
        logger.info("Retrieving assistant response")
        messages = client.beta.threads.messages.list(thread_id=thread.id)
        last_message = messages.data[0]
        
        return last_message.content[0].text.value

    except Exception as e:
        logger.error(f"Error processing message: {str(e)}", exc_info=True)
        return f"Sorry, I encountered an error: {str(e)}"

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    logger.info(f"New WebSocket connection from client {client_id}")
    
    try:
        while True:
            # Receive message from client
            message = await websocket.receive_text()
            logger.info(f"Received message from client {client_id}: {message}")
            
            # Process message with OpenAI assistant
            response = await process_message_with_assistant(message, client_id)
            
            # Send response back to client
            await websocket.send_text(response)
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
    finally:
        await websocket.close()
        logger.info(f"WebSocket connection closed for client {client_id}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 