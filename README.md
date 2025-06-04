# Email Judge Agent

A news reporter agent built with the Agno framework that delivers news with NYC flair and enthusiasm!

## Setup

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Environment Configuration
Create a `.env` file in the project root with your OpenAI API key:

```bash
# .env
OPENAI_API_KEY=your_openai_api_key_here
```

**Optional environment variables:**
```bash
# Set default model (already specified in code as gpt-4o)
OPENAI_MODEL=gpt-4o

# OpenAI Organization ID (if using organization account)
OPENAI_ORG_ID=your_org_id_here
```

### 3. Get Your OpenAI API Key
1. Go to [OpenAI's API platform](https://platform.openai.com/)
2. Sign up or log in to your account
3. Navigate to API Keys section
4. Create a new secret key
5. Copy the key and add it to your `.env` file

### 4. Run the Application
```bash
python emailjudge.py
```

## Usage

The agent comes with several example prompts you can try:
1. "What's the latest food trend taking over Brooklyn?"
2. "Tell me about a peculiar incident on the subway today"
3. "What's the scoop on the newest rooftop garden in Manhattan?"
4. "Report on an unusual traffic jam caused by escaped zoo animals"
5. "Cover a flash mob wedding proposal at Grand Central"

## Features

- 🗽 NYC-style news reporting with personality
- 📰 Attention-grabbing headlines with emoji
- 🎭 Mix of witty comedy and sharp journalism
- 🏙️ Local NYC references and slang
- ✅ Fact verification while maintaining energy

## Requirements

- Python 3.7+
- OpenAI API key
- Internet connection for API calls 