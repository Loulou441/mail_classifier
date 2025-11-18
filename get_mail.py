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
            flow = InstalledAppFlow.from_client_secrets_file('credentials_bis.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Sauvegarde pour la prochaine fois
        with open('token.json', 'w') as token:
            token.write(creds.to_json())
    service = build('gmail', 'v1', credentials=creds)
    return service

def list_message_ids(service, user_id='me', q='from:horairyhakim@gmail.com'):
    """Get all IDs messages, with pagination"""
    all_ids = []
    request = service.users().messages().list(userId=user_id, q=q, maxResults=500)
    while request:
        response = request.execute()
        messages = response.get('messages', [])
        all_ids.extend(messages)
        # Vérifie s’il y a une page suivante
        request = service.users().messages().list_next(request, response)
    return all_ids


def get_message(service, msg_id, user_id='me'):
    """Get one mail and parses it"""
    msg = service.users().messages().get(userId=user_id, id=msg_id, format='raw').execute()
    raw = base64.urlsafe_b64decode(msg['raw'])
    email_obj = BytesParser(policy=policy.default).parsebytes(raw)

    # Mail subject
    subject = email_obj['subject']
    # Mail body
    body = ""
    if email_obj.is_multipart():
        for part in email_obj.walk():
            ctype = part.get_content_type()
            if ctype == 'text/plain' and part.get_content_disposition() in (None, 'inline'):
                body = part.get_content().strip()
                break
    else:
        body = email_obj.get_content().strip()

    return {
        "subject": subject,
        "body": body
    }

def get_mails_list():
    service = get_service()
    all_ids = list_message_ids(service)
    print(f"Nombre total de mails : {len(all_ids)}")

    emails_data = []
    for i, m in enumerate(all_ids, 1):
        try:
            email_data = get_message(service, m['id'])
            emails_data.append(email_data)
            if i % 50 == 0:
                print(f"{i} mails récupérés...")
        except Exception as e:
            print(f"Erreur sur le mail {m['id']}: {e}")

    return emails_data
