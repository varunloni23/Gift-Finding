"""
FastAPI application for the Gift-Finding Chatbot.
Main entry point for the serverless backend.
"""

import uuid
from datetime import datetime
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.models import (
    ChatRequest,
    ChatResponse,
    HealthResponse,
    SuggestionChip
)
from app.database import SupabaseService
from app.agents import get_gift_suggestion, generate_suggestion_chips
from app.config import get_settings


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan handler."""
    # Startup
    print("🎁 Gift-Finding Chatbot starting up...")
    yield
    # Shutdown
    print("👋 Gift-Finding Chatbot shutting down...")


# Create FastAPI app
app = FastAPI(
    title="Gift-Finding Chatbot API",
    description="A conversational AI chatbot that helps users find personalized gift suggestions.",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend access
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "https://*.vercel.app",
        "*"  # Allow all origins in development
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/", response_model=HealthResponse)
async def root():
    """Root endpoint - health check."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.utcnow(),
        version="1.0.0"
    )


@app.post("/api/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    """
    Main chat endpoint.
    
    Accepts a user message, retrieves conversation history from Supabase,
    generates a response using the Pydantic AI agent, and returns
    the response along with suggestion chips.
    """
    try:
        # Get or create conversation ID
        conversation_id = request.conversation_id or str(uuid.uuid4())
        
        # Retrieve conversation history from Supabase
        history_messages = await SupabaseService.get_conversation_history(conversation_id)
        conversation_history = SupabaseService.format_history_for_agent(history_messages)
        
        # Save user message to Supabase
        await SupabaseService.save_message(
            conversation_id=conversation_id,
            role="user",
            content=request.message
        )
        
        # Get response from the gift suggestion agent
        agent_response = await get_gift_suggestion(
            user_message=request.message,
            conversation_history=conversation_history
        )
        
        # Save assistant response to Supabase
        await SupabaseService.save_message(
            conversation_id=conversation_id,
            role="assistant",
            content=agent_response
        )
        
        # Update conversation history for chips generation
        updated_history = conversation_history + f"\nUser: {request.message}\nAssistant: {agent_response}"
        
        # Generate suggestion chips using the sub-agent
        suggestion_chips = await generate_suggestion_chips(
            conversation_context=updated_history,
            last_assistant_message=agent_response
        )
        
        return ChatResponse(
            response=agent_response,
            suggestion_chips=suggestion_chips,
            conversation_id=conversation_id
        )
        
    except Exception as e:
        print(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred while processing your request: {str(e)}"
        )


@app.post("/api/conversations/new")
async def create_conversation():
    """Create a new conversation and return its ID."""
    conversation_id = await SupabaseService.create_conversation()
    return {"conversation_id": conversation_id}


@app.get("/api/conversations/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """Get the history of a specific conversation."""
    try:
        messages = await SupabaseService.get_conversation_history(conversation_id)
        return {
            "conversation_id": conversation_id,
            "messages": [
                {
                    "role": msg.role,
                    "content": msg.content,
                    "timestamp": msg.timestamp.isoformat() if msg.timestamp else None
                }
                for msg in messages
            ]
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving conversation history: {str(e)}"
        )


@app.delete("/api/conversations/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete a conversation and all its messages."""
    try:
        await SupabaseService.delete_conversation(conversation_id)
        return {"status": "deleted", "conversation_id": conversation_id}
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error deleting conversation: {str(e)}"
        )


@app.get("/api/suggestions/initial")
async def get_initial_suggestions():
    """Get initial suggestion chips for starting a conversation."""
    return {
        "suggestions": [
            SuggestionChip(text="Gift for my mom", type="starter"),
            SuggestionChip(text="Birthday present ideas", type="starter"),
            SuggestionChip(text="Gifts under $50", type="starter"),
            SuggestionChip(text="Unique gift ideas", type="starter"),
            SuggestionChip(text="Last-minute gift help", type="starter"),
        ]
    }


# For local development with uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
