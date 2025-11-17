import os
from groq import Groq
from dotenv import load_dotenv
from email_classifier import EmailClassifier
import json

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")
model_name = os.getenv("MODEL_NAME")

# prompt = """
# You are an AI assistant specialized in analyzing and classifying emails.

# Your job is to:
# 1. Determine the priority of the email.
# 2. Provide a short summary.
# 3. Follow all provided rules strictly.
# 4. Always respond in valid JSON.

# Be concise, accurate, and logical.
# """

# rules = """
# Priority Rules:
# - Priority 1: Emails mentioning urgent issues, deadlines, blocked processes, or financial risks.
# - Priority 2: Emails concerning meetings, planning, or coordination tasks.
# - Priority 3: Emails that are informational, newsletters, or low-impact updates.

# Additional Rules:
# - The summary must be 2 to 3 sentences maximum.
# - Never invent information not present in the email.
# - If unclear, choose the lowest reasonable priority.
# """

#Lire le prompt
f = open('../prompt.txt', 'r')
prompt = f.read()
f.close()

#Lire les règles
f = open('../rules.txt', 'r')
rules = f.read()
f.close()

emails = []
with open('../dummy.json',"r", encoding="utf-8") as f:

	emails = json.load(f)['emails']

if __name__ == "__main__":
    classifier = EmailClassifier(api_key,model_name,True)
    classified = classifier.classify_emails(emails, prompt, rules)
    print(json.dumps(classified, indent=2))