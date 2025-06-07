import streamlit as st
import os
from textwrap import dedent
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Load environment variables and set page config
load_dotenv()
st.set_page_config(page_title="Email Classifier", page_icon="📧")

# Initialize the agent (only once when the app loads)
@st.cache_resource
def initialize_agent():
    openai_api_key = os.getenv("OPENAI_API_KEY")
    if not openai_api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
        
    return Agent(
        model=OpenAIChat(
            id="gpt-4o",
            api_key=openai_api_key
        ),
        instructions=dedent("""\
            You are an intelligent email judge specifically designed for computer science students! 📧⚖
            
            Your primary role is to analyze email content and determine if it's IMPORTANT or JUNK for a CS student.

            *Classification Guidelines:*
            
            IMPORTANT emails include:
            - Academic announcements (grades, assignments, deadlines, course updates)
            - Career opportunities (internships, job postings, career fairs)
            - Technical conferences, workshops, or seminars
            - Research opportunities or lab positions
            - Scholarship and funding opportunities
            - University administrative messages (registration, tuition, housing)
            - Tech industry news or opportunities from legitimate sources
            - Professional networking requests
            - Project collaboration invitations
            - Technical learning resources or course materials

            JUNK emails include:
            - Generic promotional content
            - Unrelated product advertisements
            - Spam or phishing attempts
            - Non-academic newsletters you didn't subscribe to
            - Social media notifications (unless academic/professional)
            - Generic marketing emails
            - Irrelevant services or products

            *Response Format:*
            1. *Classification:* Start with either "📌 IMPORTANT" or "🗑 JUNK"
            2. *Reasoning:* Brief explanation (1-2 sentences) of why you classified it this way
            3. *Summary & Action Items:* (ONLY for IMPORTANT emails) Provide a concise summary with specific action items needed

            Keep your analysis sharp, concise, and student-focused!\
        """),
        markdown=True,
    )

# Create the Streamlit UI
st.title("📧 Email Classifier for CS Students")
st.write("Paste your email content below to classify it as Important or Junk")

# Create a text area for email input
email_content = st.text_area(
    "Email Content",
    height=300,
    placeholder="Paste your email content here..."
)

# Create a button to trigger classification
if st.button("Classify Email", type="primary"):
    if email_content.strip():
        # Show a spinner while processing
        with st.spinner("Analyzing email content..."):
            try:
                # Get the agent instance
                agent = initialize_agent()
                
                # Get the response using run() instead of print_response()
                response = agent.run(email_content)
                
                # Display the response in a nice format
                st.markdown("---")
                st.markdown("### Analysis Result")
                st.markdown(response.content)
                
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    else:
        st.warning("Please paste some email content first!")

# Add some helpful information at the bottom
st.markdown("---")
st.markdown("""
### 💡 Tips
- Make sure to include the email subject and body for best results
- The classifier works best with complete email content
- For accurate classification, include any relevant context
""")
