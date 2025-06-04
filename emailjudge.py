import os
from textwrap import dedent
from dotenv import load_dotenv

from agno.agent import Agent
from agno.models.openai import OpenAIChat

# Load environment variables from .env file
load_dotenv()

# Get OpenAI API key from environment
openai_api_key = os.getenv("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables. Please check your .env file.")

# Create our Email Judge Agent for CS Students
agent = Agent(
    model=OpenAIChat(
        id="gpt-4o",
        api_key=openai_api_key
    ),
    instructions=dedent("""\
        You are an intelligent email judge specifically designed for computer science students! 📧⚖️
        
        Your primary role is to analyze email content and determine if it's IMPORTANT or JUNK for a CS student.

        **Classification Guidelines:**
        
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

        **Response Format:**
        1. **Classification:** Start with either "📌 IMPORTANT" or "🗑️ JUNK"
        2. **Reasoning:** Brief explanation (1-2 sentences) of why you classified it this way
        3. **Summary & Action Items:** (ONLY for IMPORTANT emails) Provide a concise summary with specific action items needed

        Keep your analysis sharp, concise, and student-focused!\
    """),
    markdown=True,
)

# Example usage
agent.print_response(
    """
    Subject: Spring 2024 CS Department Internship Fair - March 15th
    
    Dear Computer Science Students,
    
    The CS Department is hosting our annual Internship Fair on March 15th from 10 AM to 4 PM in the Student Union. 
    Over 50 tech companies will be present including Google, Microsoft, Apple, and local startups.
    
    Please bring multiple copies of your resume and dress professionally. 
    Registration is required by March 10th through the career portal.
    
    Best regards,
    CS Career Services
    """, 
    stream=True
)

print("\n" + "="*50 + "\n")

# Example of a spam email to test JUNK classification
agent.print_response(
    """
    Subject: 🔥 URGENT! Make $5000/Week Working From Home!!! 💰💰💰
    
    Dear Friend,
    
    Congratulations! You have been SPECIALLY SELECTED for this AMAZING opportunity!!!
    
    My name is Sarah and I was just like you - struggling with student loans and bills. But then I discovered this INCREDIBLE system that changed my life FOREVER!
    
    ✅ Work only 2 hours per day
    ✅ No experience required  
    ✅ Make $5000+ per week GUARANTEED
    ✅ 100% legitimate (not a scam!)
    
    This offer expires in 24 HOURS! Don't miss out on this life-changing opportunity!
    
    Click here NOW to claim your spot: www.totally-not-a-scam.biz/get-rich-quick
    
    Limited spots available! Act FAST!
    
    Best wishes,
    Sarah Johnson
    "Former broke student, now millionaire!"
    
    P.S. This email is sent to a limited number of people. You're one of the lucky few!
    """, 
    stream=True
)

# More example emails to try:
"""
Try these email scenarios:
1. University tuition deadline reminder
2. Generic marketing email for a coding bootcamp
3. Research assistant position opening in AI lab
4. Social media platform promotional email
5. Scholarship application deadline notification
6. Random product advertisement email
"""