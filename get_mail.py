# gmail_read.py
import base64
import os.path
from email import policy
from email.parser import BytesParser

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Lecture des emails
SCOPES = ['https://www.googleapis.com/auth/gmail.readonly']

def get_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # Si pas de credentials valides, lancer le flow OAuth
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Sauvegarde pour la prochaine fois
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_message_ids(service, user_id='me', q=None):
    """Retourne une liste d'ids de messages. q est une query Gmail (ex: 'is:unread from:boss@example.com')."""
    response = service.users().messages().list(userId=user_id, q=q).execute()
    return response.get('messages', [])

def get_message(service, msg_id, user_id='me'):
    """Récupère le message complet (raw) et le parse en objet email."""
    msg = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    raw = base64.urlsafe_b64decode(msg['raw'])
    email_obj = BytesParser(policy=policy.default).parsebytes(raw)
    return email_obj

def main():
    service = get_service()
    # Récupérer les mails
    ids = list_message_ids(service)
    print(f"Trouvé {len(ids)} messages.")
    for m in ids:
        msg = get_message(service, m['id'])
        # Affiche sujet, de, date et début du corps
        subject = msg['subject']
        sender = msg['from']
        date = msg['date']
        # Récupérer le texte (plain) si présent
        body = ""
        if msg.is_multipart():
            for part in msg.walk():
                ctype = part.get_content_type()
                if ctype == 'text/plain' and part.get_content_disposition() in (None, 'inline'):
                    body = part.get_content().strip()
                    break
        else:
            body = msg.get_content().strip()
        print("-----")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")
        print("Body (début) :", body[:300].replace("\n", " "))
    print("Terminé.")

if __name__ == '__main__':
    main()