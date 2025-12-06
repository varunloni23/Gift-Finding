"""
Supabase database service for conversation memory.
Handles storing and retrieving conversation history.
"""

import uuid
from datetime import datetime
from typing import Optional
from supabase import create_client, Client
from app.config import get_settings
from app.models import ChatMessage, ConversationHistory


class SupabaseService:
    """Service class for Supabase database operations."""
    
    _client: Optional[Client] = None
    
    @classmethod
    def get_client(cls) -> Client:
        """Get or create Supabase client (singleton pattern for serverless)."""
        if cls._client is None:
            settings = get_settings()
            cls._client = create_client(settings.supabase_url, settings.supabase_key)
        return cls._client
    
    @classmethod
    async def create_conversation(cls) -> str:
        """Create a new conversation and return its ID."""
        conversation_id = str(uuid.uuid4())
        return conversation_id
    
    @classmethod
    async def save_message(
        cls,
        conversation_id: str,
        role: str,
        content: str
    ):
        """
        Save a message to the conversation history.
        
        Args:
            conversation_id: Unique identifier for the conversation
            role: 'user' or 'assistant'
            content: The message content
            
        Returns:
            The saved message record
        """
        client = cls.get_client()
        
        message_data = {
            "conversation_id": conversation_id,
            "role": role,
            "content": content,
            "created_at": datetime.utcnow().isoformat()
        }
        
        result = client.table("conversation_messages").insert(message_data).execute()
        return result.data[0] if result.data else message_data
    
    @classmethod
    async def get_conversation_history(
        cls,
        conversation_id: str,
        limit: Optional[int] = None
    ) -> list[ChatMessage]:
        """
        Retrieve conversation history for a given conversation ID.
        
        Args:
            conversation_id: The conversation to retrieve
            limit: Maximum number of messages to return
            
        Returns:
            List of ChatMessage objects in chronological order
        """
        settings = get_settings()
        client = cls.get_client()
        
        query = client.table("conversation_messages").select("*").eq(
            "conversation_id", conversation_id
        ).order("created_at", desc=False)
        
        if limit:
            query = query.limit(limit)
        else:
            query = query.limit(settings.max_conversation_history)
        
        result = query.execute()
        
        messages = []
        if result.data:
            for row in result.data:
                # Ensure row is a dict before accessing keys
                if isinstance(row, dict):
                    messages.append(ChatMessage(
                        role=str(row.get("role", "")),
                        content=str(row.get("content", "")),
                        timestamp=datetime.fromisoformat(row["created_at"]) if row.get("created_at") else None
                    ))
        
        return messages
    
    @classmethod
    async def delete_conversation(cls, conversation_id: str) -> bool:
        """
        Delete all messages in a conversation.
        
        Args:
            conversation_id: The conversation to delete
            
        Returns:
            True if successful
        """
        client = cls.get_client()
        client.table("conversation_messages").delete().eq(
            "conversation_id", conversation_id
        ).execute()
        return True
    
    @classmethod
    def format_history_for_agent(cls, messages: list[ChatMessage]) -> str:
        """
        Format conversation history as a string for the agent context.
        
        Args:
            messages: List of chat messages
            
        Returns:
            Formatted string of conversation history
        """
        if not messages:
            return "No previous conversation history."
        
        formatted = []
        for msg in messages:
            role_label = "User" if msg.role == "user" else "Assistant"
            formatted.append(f"{role_label}: {msg.content}")
        
        return "\n".join(formatted)


# SQL Schema for Supabase (run this in Supabase SQL editor)
SUPABASE_SCHEMA = """
-- Create the conversation_messages table
CREATE TABLE IF NOT EXISTS conversation_messages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    conversation_id UUID NOT NULL,
    role TEXT NOT NULL CHECK (role IN ('user', 'assistant')),
    content TEXT NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    
    -- Index for faster queries
    CONSTRAINT valid_role CHECK (role IN ('user', 'assistant'))
);

-- Create index for faster conversation lookups
CREATE INDEX IF NOT EXISTS idx_conversation_messages_conversation_id 
ON conversation_messages(conversation_id);

-- Create index for timestamp ordering
CREATE INDEX IF NOT EXISTS idx_conversation_messages_created_at 
ON conversation_messages(created_at);

-- Enable Row Level Security (optional but recommended)
ALTER TABLE conversation_messages ENABLE ROW LEVEL SECURITY;

-- Create a policy that allows all operations (adjust based on your auth needs)
CREATE POLICY "Allow all operations" ON conversation_messages
    FOR ALL USING (true) WITH CHECK (true);
"""
