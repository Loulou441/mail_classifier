import gspread
from google.oauth2.service_account import Credentials

# from settings import SERVICE_ACCOUNT_FILE, SPREADSHEET_NAME
from config import *
print('service account file',SERVICE_ACCOUNT_FILE)



def get_client():
    """Initialise et retourne le client Google Sheets"""
    creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
    client = gspread.authorize(creds)
    return client

def get_spreadsheet():
    """Retourne le spreadsheet"""
    client = get_client()
    return client.open(SPREADSHEET_NAME)

def write_ticket(ticket_data):
    """
    Écrit un ticket dans le Google Sheet.
    
    ticket_data = {
        "subject": "...",
        "category": "...",
        "urgency": "...",
        "summary": "..."
    }
    """
    try:
        # Obtenir le spreadsheet
        spreadsheet = get_spreadsheet()
        
        # Récupérer ou créer l'onglet
        try:
            sheet = spreadsheet.worksheet(ticket_data["category"])
            print(f"📄 Onglet '{ticket_data['category']}' trouvé")
        except gspread.WorksheetNotFound:
            print(f"📝 Création de l'onglet '{ticket_data['category']}'")
            sheet = spreadsheet.add_worksheet(
                title=ticket_data["category"], 
                rows=1000, 
                cols=10
            )
        
        # Vérifier et ajouter l'en-tête si nécessaire
        all_values = sheet.get_all_values()
        
        # Si la feuille est vide ou n'a pas le bon en-tête
        if len(all_values) == 0:
            print("📋 Ajout de l'en-tête")
            sheet.append_row(["Sujet", "Urgence", "Synthèse"])
        elif all_values[0] != ["Sujet", "Urgence", "Synthèse"]:
            print("📋 Correction de l'en-tête")
            sheet.insert_row(["Sujet", "Urgence", "Synthèse"], index=1)
        
        # Ajouter le ticket
        sheet.append_row([
            ticket_data["subject"],
            ticket_data["urgency"],
            ticket_data["summary"]
        ])
        
        print(f"✅ Ticket écrit dans '{ticket_data['category']}'")
        return True
        
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Erreur : Spreadsheet '{SPREADSHEET_NAME}' introuvable")
        print(f"⚠️  Vérifiez que le spreadsheet existe et que le compte service y a accès")
        print(f"⚠️  Email du service account : sheet-writer@mail-agent-478513.iam.gserviceaccount.com")
        return False
    except gspread.exceptions.APIError as e:
        print(f"❌ Erreur API Google : {e}")
        return False
    except Exception as e:
        print(f"❌ Erreur inattendue : {type(e).__name__} - {e}")
        return False

def verify_spreadsheet_connection():
    """
    Vérifie la connexion au spreadsheet et affiche les onglets existants.
    """
    try:
        spreadsheet = get_spreadsheet()
        print(f"✅ Connexion réussie au spreadsheet : '{spreadsheet.title}'")
        print(f"📊 URL : {spreadsheet.url}")
        print(f"📊 Onglets existants :")
        
        worksheets = spreadsheet.worksheets()
        if len(worksheets) == 0:
            print("   (Aucun onglet)")
        else:
            for ws in worksheets:
                row_count = len(ws.get_all_values())
                print(f"   - {ws.title} : {row_count} lignes")
        
        print(f"\n💡 Email du service account à partager :")
        print(f"   sheet-writer@mail-agent-478513.iam.gserviceaccount.com")
        
        return True
        
    except gspread.exceptions.SpreadsheetNotFound:
        print(f"❌ Spreadsheet '{SPREADSHEET_NAME}' introuvable")
        print(f"\n🔧 Solutions possibles :")
        print(f"   1. Vérifiez que le nom est exact (sensible à la casse)")
        print(f"   2. Partagez le spreadsheet avec : sheet-writer@mail-agent-478513.iam.gserviceaccount.com")
        print(f"   3. Donnez les droits 'Éditeur' au compte service")
        return False
        
    except Exception as e:
        print(f"❌ Erreur de connexion : {type(e).__name__}")
        print(f"   Détails : {e}")
        return False

def create_all_category_sheets():
    """
    Crée tous les onglets de catégories s'ils n'existent pas.
    Utile pour initialiser le spreadsheet.
    """
    from settings import CATEGORIES
    
    try:
        spreadsheet = get_spreadsheet()
        print(f"📊 Initialisation des onglets pour : {spreadsheet.title}\n")
        
        for category in CATEGORIES:
            try:
                sheet = spreadsheet.worksheet(category)
                print(f"✓ Onglet '{category}' existe déjà")
            except gspread.WorksheetNotFound:
                print(f"+ Création de l'onglet '{category}'")
                sheet = spreadsheet.add_worksheet(title=category, rows=1000, cols=10)
                # Ajouter l'en-tête
                sheet.append_row(["Sujet", "Urgence", "Synthèse"])
                print(f"  ✓ En-tête ajouté")
        
        print(f"\n✅ Tous les onglets sont prêts !")
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la création des onglets : {e}")
        return False