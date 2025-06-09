import streamlit as st
from agno.agent import Agent
from agno.memory.v2.db.sqlite import SqliteMemoryDb
from agno.memory.v2.memory import Memory
from agno.models.openai import OpenAIChat
from agno.storage.sqlite import SqliteStorage
from rich.pretty import pprint
from dotenv import load_dotenv
import os
from textwrap import dedent
from typing import Optional

load_dotenv()

def get_agent(user_id: str, session_id: Optional[str] = None, db_file="tmp/agent.db"):
    """Create an agent with proper memory configuration based on Agno docs"""
    
    # Initialize memory system with SQLite storage (as per Agno docs)
    memory = Memory(
        model=OpenAIChat(id="gpt-4o"),  # Using gpt-4o as recommended in docs
        db=SqliteMemoryDb(
            table_name="agent_memory",
            db_file=db_file,
        ),
    )
    
    # Initialize storage for agent sessions
    agent_storage = SqliteStorage(
        table_name="agent_sessions", 
        db_file=db_file
    )
    
    # Create agent with enhanced memory configuration
    agent = Agent(
        model=OpenAIChat(id="gpt-4o"),
        user_id=user_id,
        session_id=session_id,
        memory=memory,
        storage=agent_storage,
        enable_user_memories=True,
        enable_session_summaries=True,
        add_memory_references=True,  # Add existing memories to context
        add_history_to_messages=True,
        num_history_responses=5,  # Increased for better context
        markdown=True,
        # Enhanced system prompt for better memory usage
        description=dedent("""\
            You are a helpful and friendly AI assistant with excellent memory.
            - Remember important details about users and reference them naturally
            - Maintain a warm, positive tone while being precise and helpful  
            - When appropriate, refer back to previous conversations and memories
            - Always be truthful about what you remember or don't remember
            - Keep responses conversational and engaging"""),
    )
    
    return agent, memory

def get_existing_user_sessions(db_file="tmp/agent.db"):
    """Get existing users and their sessions from the database"""
    try:
        agent_storage = SqliteStorage(table_name="agent_sessions", db_file=db_file)
        
        # Try to get all users who have had sessions
        all_sessions = agent_storage.get_all_sessions()
        
        if all_sessions:
            # Get the most recent session's user_id
            latest_session = max(all_sessions, key=lambda x: x.get('created_at', ''))
            return latest_session.get('user_id'), latest_session.get('session_id')
        
        return None, None
    except Exception as e:
        print(f"Error getting existing sessions: {e}")
        return None, None

def get_last_user_from_memory(db_file="tmp/agent.db"):
    """Get the most recent user from memory database"""
    try:
        import sqlite3
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Check if the table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='agent_memory'")
        if not cursor.fetchone():
            conn.close()
            return None
            
        # Get the most recent user from agent_memory table
        cursor.execute("SELECT DISTINCT user_id FROM agent_memory ORDER BY created_at DESC LIMIT 1")
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        return None
    except Exception as e:
        print(f"Error getting last user from memory: {e}")
        return None

def generate_greeting(user_id: str, agent: Agent):
    """Generate a personalized greeting based on user's memory"""
    try:
        # Check if user has existing memories
        memories = agent.memory.get_user_memories(user_id=user_id)
        
        if memories and user_id and user_id != "User":
            # Simple, natural greeting for returning users
            greeting = f"Hello {user_id}! What would you like to discuss today?"
        else:
            # Greeting for new users
            greeting = "Hello! I'm your AI assistant. What would you like to talk about today?"
            
        return greeting
    except Exception as e:
        print(f"Error generating greeting: {e}")
        return "Hello! I'm your AI assistant. What would you like to talk about today?"

st.set_page_config(page_title="AI Chat", page_icon="🤖")
st.title("AI Chat")

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_id" not in st.session_state:
    st.session_state.user_id = None

if "session_id" not in st.session_state:
    st.session_state.session_id = None

if "agent" not in st.session_state:
    st.session_state.agent = None

if "initialized" not in st.session_state:
    st.session_state.initialized = False

# Auto-initialize with existing user or prepare for new user
if not st.session_state.initialized:
    # Try to get existing user from memory database
    existing_user = get_last_user_from_memory()
    
    if existing_user:
        # Load existing user
        st.session_state.user_id = existing_user
        
        # Get existing sessions for this user
        agent_storage = SqliteStorage(table_name="agent_sessions", db_file="tmp/agent.db")
        try:
            existing_sessions = agent_storage.get_all_session_ids(existing_user)
            if existing_sessions:
                st.session_state.session_id = existing_sessions[0]  # Use most recent session
        except:
            st.session_state.session_id = None
        
        # Create agent with existing user context
        agent, memory = get_agent(st.session_state.user_id, st.session_state.session_id)
        st.session_state.agent = agent
        
        # Generate personalized greeting
        greeting = generate_greeting(st.session_state.user_id, agent)
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    else:
        # New user - just show initial greeting
        greeting = "Hello! I'm your AI assistant. Please tell me your name so I can remember you for future conversations."
        st.session_state.messages.append({"role": "assistant", "content": greeting})
    
    st.session_state.initialized = True

# Display all chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Type your message..."):
    # Handle first message for new users (extract user name)
    if st.session_state.user_id is None:
        # Extract user name from first message
        words = prompt.split()
        if len(words) > 0:
            # Try to extract name intelligently
            if "name is" in prompt.lower():
                name_index = prompt.lower().find("name is") + 8
                potential_name = prompt[name_index:].split()[0].strip('.,!?')
                st.session_state.user_id = potential_name
            elif "i'm" in prompt.lower():
                im_index = prompt.lower().find("i'm") + 4
                potential_name = prompt[im_index:].split()[0].strip('.,!?')
                st.session_state.user_id = potential_name
            elif "i am" in prompt.lower():
                iam_index = prompt.lower().find("i am") + 5
                potential_name = prompt[iam_index:].split()[0].strip('.,!?')
                st.session_state.user_id = potential_name
            else:
                # Use first word as fallback
                st.session_state.user_id = words[0].strip('.,!?')
        
        # Create new agent for this user
        agent, memory = get_agent(st.session_state.user_id)
        st.session_state.agent = agent
        st.session_state.session_id = agent.session_id

    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    # Generate AI response using the agent
    try:
        if st.session_state.agent:
            response = st.session_state.agent.run(
                message=prompt,
                user_id=st.session_state.user_id
            )
            
            if hasattr(response, "content"):
                response_content = response.content
            else:
                response_content = str(response)
        else:
            response_content = "I'm sorry, there was an issue initializing the agent. Please refresh the page."
            
    except Exception as e:
        response_content = f"I encountered an error: {str(e)}. Please try again."
        print(f"Agent error: {e}")
    
    # Add AI response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response_content})
    with st.chat_message("assistant"):
        st.markdown(response_content)