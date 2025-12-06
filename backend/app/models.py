"""
Pydantic models for the Gift-Finding Chatbot API.
"""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    """Represents a single chat message."""
    role: str = Field(..., description="Role of the message sender: 'user' or 'assistant'")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default=None, description="When the message was created")


class ChatRequest(BaseModel):
    """Request model for chat endpoint."""
    message: str = Field(..., description="User's message to the chatbot")
    conversation_id: Optional[str] = Field(default=None, description="ID for conversation continuity")


class SuggestionChip(BaseModel):
    """Represents a quick reply suggestion chip."""
    text: str = Field(..., description="The suggestion text to display")
    type: str = Field(default="suggestion", description="Type of chip: suggestion, category, etc.")


class GiftSuggestion(BaseModel):
    """Represents a gift suggestion from the agent."""
    gift_name: str = Field(..., description="Name of the suggested gift")
    description: str = Field(..., description="Why this gift would be good")
    price_range: Optional[str] = Field(default=None, description="Approximate price range")
    category: Optional[str] = Field(default=None, description="Gift category")


class AgentResponse(BaseModel):
    """Response from the gift suggestion agent."""
    message: str = Field(..., description="The agent's response message")
    suggestions: list[GiftSuggestion] = Field(default_factory=list, description="Gift suggestions if any")


class ChatResponse(BaseModel):
    """Response model for chat endpoint."""
    response: str = Field(..., description="The chatbot's response")
    suggestion_chips: list[SuggestionChip] = Field(default_factory=list, description="Quick reply suggestions")
    conversation_id: str = Field(..., description="Conversation ID for continuity")


class ConversationHistory(BaseModel):
    """Model for conversation history stored in Supabase."""
    id: Optional[str] = None
    conversation_id: str
    role: str
    content: str
    created_at: Optional[datetime] = None


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    timestamp: datetime
    version: str = "1.0.0"
