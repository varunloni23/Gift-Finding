"""
Pydantic AI Agents for the Gift-Finding Chatbot.
Contains the main gift suggestion agent and the suggestion chips sub-agent.
"""

import os
from typing import Optional
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from app.config import get_settings
from app.models import SuggestionChip

# Set the GEMINI_API_KEY environment variable for pydantic-ai
# This must be done before importing/using the model
_settings = get_settings()
os.environ["GEMINI_API_KEY"] = _settings.gemini_api_key


# ============================================================================
# Gift Suggestion Agent
# ============================================================================

class GiftAgentDependencies(BaseModel):
    """Dependencies/context for the gift agent."""
    conversation_history: str = Field(default="", description="Previous conversation context")
    user_preferences: Optional[dict] = Field(default=None, description="Known user preferences")


class GiftAgentResult(BaseModel):
    """Structured result from the gift agent."""
    response: str = Field(..., description="The conversational response to the user")
    gift_ideas: list[str] = Field(default_factory=list, description="List of specific gift ideas mentioned")
    needs_more_info: bool = Field(default=False, description="Whether more information is needed")
    recipient_info_gathered: dict = Field(default_factory=dict, description="Information gathered about the recipient")


def create_gift_agent() -> Agent:
    """
    Create and configure the main gift suggestion agent.
    
    Returns:
        Configured Pydantic AI Agent for gift suggestions
    """
    # Create the agent with system prompt
    # Using string model name - pydantic-ai reads GEMINI_API_KEY from environment
    agent = Agent(
        model="gemini-2.0-flash",
        system_prompt="""You are a friendly and helpful Gift-Finding Assistant. Your goal is to help users find the perfect gift for their loved ones.

## Your Personality:
- Warm, enthusiastic, and genuinely interested in helping
- Ask thoughtful follow-up questions to understand the recipient better
- Provide creative and personalized gift suggestions
- Consider budget, occasion, and relationship when making recommendations

## How to Help:
1. **Gather Information**: Ask about the recipient (age, interests, hobbies, relationship to user)
2. **Understand Context**: Ask about the occasion, budget, and any constraints
3. **Suggest Gifts**: Provide 3-5 thoughtful gift ideas with brief explanations of why each would be good
4. **Be Specific**: Give concrete product suggestions, not just categories
5. **Consider Variety**: Offer gifts at different price points and styles

## Important Guidelines:
- If the user hasn't provided enough information, ask clarifying questions
- Always explain WHY a gift would be good for that specific person
- Be encouraging and positive
- Remember context from earlier in the conversation
- If asked about something unrelated to gifts, politely redirect to gift-finding

## Response Format:
- Keep responses conversational and friendly
- Use bullet points or numbered lists for gift suggestions
- Include approximate price ranges when suggesting specific gifts
- End with a question to keep the conversation going if needed

Remember: You're not just suggesting random gifts - you're helping create meaningful moments between people!"""
    )
    
    return agent


# ============================================================================
# Suggestion Chips Sub-Agent
# ============================================================================

class ChipsAgentResult(BaseModel):
    """Result from the suggestion chips agent."""
    chips: list[str] = Field(..., description="List of 3-5 short suggestion chip texts")


def create_chips_agent() -> Agent:
    """
    Create the suggestion chips sub-agent.
    This agent generates quick reply options based on the conversation context.
    
    Returns:
        Configured Pydantic AI Agent for generating suggestion chips
    """
    # Using string model name - pydantic-ai reads GEMINI_API_KEY from environment
    agent = Agent(
        model="gemini-2.0-flash",
        system_prompt="""You are a helper agent that generates suggestion chips (quick reply buttons) for a gift-finding chatbot.

## Your Task:
Generate 3-5 short, clickable suggestion phrases that the user might want to say next in the conversation.

## Guidelines:
1. Keep each suggestion SHORT (2-6 words max)
2. Make them conversational and natural
3. Based on the conversation context, suggest logical next steps
4. Include a mix of:
   - Direct answers to questions the assistant asked
   - Follow-up questions the user might have
   - New directions the conversation could go

## Examples of Good Chips:
- "Under $50"
- "They love cooking"
- "It's for my mom"
- "Something unique"
- "Show me more options"
- "What about tech gifts?"
- "For their birthday"
- "They're into fitness"

## Important:
- ONLY output the chip texts, nothing else
- Make them relevant to where the conversation is right now
- Don't repeat suggestions
- Vary the types of suggestions offered

Output exactly 4 suggestion chips, one per line."""
    )
    
    return agent


async def generate_suggestion_chips(
    conversation_context: str,
    last_assistant_message: str
) -> list[SuggestionChip]:
    """
    Generate suggestion chips based on conversation context.
    
    Args:
        conversation_context: The conversation history
        last_assistant_message: The most recent assistant response
        
    Returns:
        List of SuggestionChip objects
    """
    chips_agent = create_chips_agent()
    
    prompt = f"""Based on this gift-finding conversation, generate 4 suggestion chips (quick reply options) for the user.

Recent conversation:
{conversation_context[-1500:] if len(conversation_context) > 1500 else conversation_context}

The assistant just said:
{last_assistant_message}

Generate 4 short, relevant suggestion chips the user might want to click:"""

    try:
        result = await chips_agent.run(prompt)
        
        # Parse the result into chips
        chip_texts = [
            line.strip().strip('-').strip('•').strip('*').strip()
            for line in result.output.strip().split('\n')
            if line.strip() and not line.strip().startswith('#')
        ]
        
        # Filter and limit to 4 chips
        chips = []
        for text in chip_texts[:4]:
            if text and len(text) < 50:  # Reasonable length limit
                chips.append(SuggestionChip(text=text, type="suggestion"))
        
        # Ensure we have at least some default chips if parsing failed
        if len(chips) < 2:
            chips = [
                SuggestionChip(text="Tell me more", type="suggestion"),
                SuggestionChip(text="Different ideas please", type="suggestion"),
                SuggestionChip(text="What's your budget?", type="suggestion"),
                SuggestionChip(text="Something unique", type="suggestion"),
            ]
        
        return chips
        
    except Exception as e:
        # Return default chips on error
        print(f"Error generating chips: {e}")
        return [
            SuggestionChip(text="Under $50", type="suggestion"),
            SuggestionChip(text="Something creative", type="suggestion"),
            SuggestionChip(text="More options", type="suggestion"),
            SuggestionChip(text="Help me decide", type="suggestion"),
        ]


async def get_gift_suggestion(
    user_message: str,
    conversation_history: str = ""
) -> str:
    """
    Get a gift suggestion response from the main agent.
    
    Args:
        user_message: The user's current message
        conversation_history: Formatted previous conversation
        
    Returns:
        The agent's response string
    """
    agent = create_gift_agent()
    
    # Build the prompt with context
    if conversation_history:
        prompt = f"""Previous conversation:
{conversation_history}

User's new message: {user_message}

Please respond to the user's message, taking into account the conversation history above."""
    else:
        prompt = user_message
    
    result = await agent.run(prompt)
    return result.output
