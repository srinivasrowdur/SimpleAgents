# Email Judge Agent 📧⚖️

An intelligent email classification agent specifically designed for computer science students! This AI-powered tool automatically analyzes your emails and determines whether they're **IMPORTANT** or **JUNK**, helping you focus on what matters for your academic and career success.

## 🎯 What It Does

The Email Judge Agent:
- ✅ **Classifies emails** as IMPORTANT or JUNK based on CS student needs
- ✅ **Summarizes important emails** with actionable next steps
- ✅ **Filters out spam** and irrelevant promotional content
- ✅ **Focuses on academic and career opportunities** relevant to CS students

## 🧠 Classification System

### 📌 **IMPORTANT Emails Include:**
- Academic announcements (grades, assignments, deadlines, course updates)
- Career opportunities (internships, job postings, career fairs)
- Technical conferences, workshops, or seminars
- Research opportunities or lab positions
- Scholarship and funding opportunities
- University administrative messages (registration, tuition, housing)
- Tech industry news from legitimate sources
- Professional networking requests
- Project collaboration invitations
- Technical learning resources

### 🗑️ **JUNK Emails Include:**
- Generic promotional content
- Unrelated product advertisements
- Spam or phishing attempts
- Non-academic newsletters
- Social media notifications (unless academic/professional)
- Generic marketing emails
- Get-rich-quick schemes

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. Get Your OpenAI API Key
1. Visit [OpenAI's API platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to the API Keys section
4. Create a new secret key
5. Copy the key and add it to your `.env` file

### 4. Run the Application
```bash
python emailjudge.py
```

## 📝 Usage Examples

The script includes two example emails to demonstrate the classification system:

1. **CS Department Internship Fair** → Classified as **📌 IMPORTANT**
   - Provides summary and action items (register by deadline, prepare resumes)

2. **Get-Rich-Quick Spam Email** → Classified as **🗑️ JUNK**
   - Explains why it's irrelevant to CS students

### Custom Usage
To analyze your own emails, modify the `agent.print_response()` call in the script with your email content:

```python
agent.print_response("""
Subject: Your Email Subject Here

Your email content here...
""", stream=True)
```

## 📋 Response Format

For each email, the agent provides:

1. **Classification**: Clear 📌 IMPORTANT or 🗑️ JUNK label
2. **Reasoning**: Brief explanation of the classification decision
3. **Summary & Action Items**: (For IMPORTANT emails only) Concise summary with specific next steps

## 🛠️ Technical Stack

- **AI Model**: OpenAI GPT-4o
- **Framework**: Agno Agent Framework
- **Environment Management**: python-dotenv
- **Language**: Python 3.7+

## 📁 Project Structure

```
EmailJudge/
├── emailjudge.py          # Main application file
├── requirements.txt       # Python dependencies
├── .env                   # Environment variables (create this)
├── .gitignore            # Git ignore rules
└── README.md             # This file
```

## 🔒 Security

- Your OpenAI API key is stored securely in the `.env` file
- The `.env` file is excluded from Git via `.gitignore`
- Never commit API keys to version control

## 🎓 Perfect for CS Students

This tool is specifically tuned for computer science students and understands:
- Academic deadlines and course requirements
- Tech industry opportunities and networking
- Research and lab positions
- Coding bootcamps vs. legitimate educational content
- Professional development in the tech field

## 🤝 Contributing

Feel free to customize the classification criteria in the agent instructions to better match your specific needs and interests!

---

**Stay focused on what matters for your CS journey!** 🎯📚 