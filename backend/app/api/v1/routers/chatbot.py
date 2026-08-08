"""
Spam Shield AI Chatbot

The chatbot automatically detects whether the user submitted:

- Website
- Email
- Phone Number
- UPI ID
- SMS / WhatsApp Message
- General Cybersecurity Question

and asks the AI to respond accordingly.
"""

import re
import json

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from app.api.deps import get_current_user
from app.models.user import User
from app.services.gemini_service import gemini_service

router = APIRouter(
    prefix="/chatbot",
    tags=["AI Chatbot"],
)


# ---------------------------------------------------------
# Request / Response
# ---------------------------------------------------------

class ChatRequest(BaseModel):
    message: str
    conversation_history: list[str] = []


class ChatResponse(BaseModel):
    reply: str


# ---------------------------------------------------------
# Detect input type
# ---------------------------------------------------------

def detect_input_type(text: str) -> str:

    text = text.strip()

    if re.search(r"https?://|www\.", text, re.IGNORECASE):
        return "website"

    if re.search(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text,
    ):
        return "email"

    if re.search(r"(\+91)?[6-9]\d{9}", text):
        return "phone"

    if re.search(r"[A-Za-z0-9._-]+@[A-Za-z]+", text):
        return "upi"

    if len(text.split()) >= 8:
        return "message"

    return "question"

def system_prompt():

    return """
You are Spam Shield AI Assistant.

You are an enterprise Cyber Security Assistant.

You specialize in:

• Phishing Detection
• Scam Detection
• Digital Forensics
• Banking Fraud
• UPI Fraud
• QR Code Fraud
• Fake Shopping Websites
• Fake Job Offers
• Investment Scams
• Malware Awareness
• Privacy Protection

Your mission is to help users stay safe online.

Rules:

1. Speak in simple English.

2. Use headings.

3. Explain WHY the result was reached.

4. Mention the risk level.

5. Mention confidence if appropriate.

6. Give practical recommendations.

7. Never invent facts.

8. If information is insufficient,
say that more verification is needed.

9. Always end with:

Safety Tips

10. Format replies like this:

## Analysis

...

## Risk Level

...

## Why

...

## Recommendation

...

## Safety Tips

...

Return ONLY JSON.

{
  "reply":"..."
}
"""
# ---------------------------------------------------------
# Extra Context Builder
# ---------------------------------------------------------

def build_extra_context(input_type: str) -> str:

    if input_type == "website":
        return """
Focus on:

• Domain reputation
• Typosquatting
• SSL usage
• Suspicious URL patterns
• Fake login pages
• Brand impersonation
• Credential theft
"""

    if input_type == "email":
        return """
Focus on:

• Phishing
• Sender spoofing
• Fake domains
• Urgency
• Credential theft
• Attachments
"""

    if input_type == "phone":
        return """
Focus on:

• Scam calls
• Spam behaviour
• Fake customer care
• OTP fraud
"""

    if input_type == "upi":
        return """
Focus on:

• Fake payment request
• UPI impersonation
• Fraudulent payment collection
"""

    if input_type == "message":
        return """
Focus on:

• SMS scams
• WhatsApp scams
• Fake KYC
• Banking fraud
• Courier scams
• Lottery scams
• QR scams
• Investment scams
"""

    return """
Answer cybersecurity questions accurately.

Educate users.

Provide practical advice.
"""

#---------------------------------------------------------
# Prompt Builder
# ---------------------------------------------------------

def build_prompt(input_type: str):

    if input_type == "website":

        return """
You are Spam Shield AI.

You are an expert cybersecurity analyst.

The user has submitted a WEBSITE.

Analyze it intelligently.

Even if you cannot verify it online, inspect:

- domain name
- spelling
- typosquatting
- phishing patterns
- fake banking
- fake shopping
- fake login pages
- suspicious keywords
- URL structure

If the domain is clearly a famous official website such as:

google.com
github.com
amazon.com
apple.com
paypal.com
facebook.com
instagram.com
microsoft.com

mark it LOW RISK.

Otherwise explain why it looks suspicious.

Return ONLY JSON.

{
"reply":"Website Analysis\n\nRisk: ...\n\nReason:\n- ...\n\nRecommendation:\n- ..."
}
"""

    elif input_type == "email":

        return """
You are Spam Shield AI.

Analyze the email.

Check for:

- phishing
- spoofing
- fake domains
- urgency
- credential theft

Return ONLY JSON.

{
"reply":"Email Analysis..."
}
"""

    elif input_type == "phone":

        return """
You are Spam Shield AI.

Analyze this phone number.

Look for:

- scam likelihood
- spam behaviour
- fake support possibility

Return ONLY JSON.

{
"reply":"Phone Analysis..."
}
"""

    elif input_type == "upi":

        return """
You are Spam Shield AI.

Analyze this UPI ID.

Check for:

- fake payment request
- suspicious naming
- impersonation

Return ONLY JSON.

{
"reply":"UPI Analysis..."
}
"""

    elif input_type == "message":

        return """
You are Spam Shield AI.

Analyze this SMS / WhatsApp message.

Look for:

- phishing
- OTP scam
- fake KYC
- fake bank
- courier scam
- investment scam
- job scam
- lottery scam
- QR scam
- urgency
- suspicious links

Return ONLY JSON.

{
"reply":"Message Analysis..."
}
"""

    return """
You are Spam Shield AI.

Answer cybersecurity questions.

Rules:

Give practical advice.

Be concise.

Use bullet points when appropriate.

Never invent facts.

Return ONLY JSON.

{
"reply":"..."
}
"""


# ---------------------------------------------------------
# Endpoint
# ---------------------------------------------------------

@router.post(
    "/message",
    response_model=ChatResponse,
)
async def chat(
    payload: ChatRequest,
    current_user: User = Depends(get_current_user),
):

    input_type = detect_input_type(payload.message)

    history = "\n".join(
    payload.conversation_history[-10:]
    )

    context = f"""
Conversation History:

{history}

Detected Input Type:

{input_type}

Additional Instructions:

{build_extra_context(input_type)}

User Message:

{payload.message}
"""

    result = await gemini_service.generate_structured(
        task_prompt=system_prompt() + "\n\n" + build_prompt(input_type),
        untrusted_content=context,
        response_schema_hint="""
{
"reply":"string"
}
""",
    )

    print("=" * 80)
    print("CHATBOT RESULT")
    print(result)
    print("=" * 80)

    # ---------------------------------------------------------
# Post Process AI Response
# ---------------------------------------------------------

    reply = result.get(
        "reply",
        "Sorry, I couldn't analyze your request.",
    )

    reply = reply.strip()

    if not reply.endswith("Stay safe online!"):
        reply += """

    ━━━━━━━━━━━━━━━━━━━━━━

    🛡 Spam Shield AI Recommendation

    • Never share OTPs or passwords.
    • Verify unknown websites before logging in.
    • Do not scan QR codes from unknown sources.
    • Never transfer money without verification.

    Stay safe online!
    """

    if result.get("_fallback"):
        return ChatResponse(
            reply="⚠️ AI Assistant is temporarily unavailable. Please try again."
        )

    return ChatResponse(
    reply=reply
)
    
