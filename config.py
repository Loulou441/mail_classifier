from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GROQ_API_KEY")
MODEL_NAME = os.getenv("MODEL_NAME")
SPREADSHEET_NAME = os.getenv("SPREADSHEET_NAME")
SERVICE_ACCOUNT_FILE = os.getenv('SERVICE_ACCOUNT_FILE')

CATEGORIES = [
    "Problème technique informatique",
    "Demande administrative",
    "Problème d’accès / authentification",
    "Demande de support utilisateur",
    "Bug ou dysfonctionnement d’un service"
]
