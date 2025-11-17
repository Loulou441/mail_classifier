"""
Script de test pour vérifier l'écriture dans Google Sheets
"""
from sheets_writer import verify_spreadsheet_connection, write_ticket, create_all_category_sheets

def test_1_connection():
    """Test 1 : Vérifier la connexion"""
    print("\n" + "="*70)
    print("TEST 1 : VÉRIFICATION DE LA CONNEXION")
    print("="*70)
    
    result = verify_spreadsheet_connection()
    
    if not result:
        print("\n❌ ÉCHEC : Impossible de se connecter au spreadsheet")
        print("\n🔧 ACTIONS À FAIRE :")
        print("   1. Ouvrez le Google Sheet dans votre navigateur")
        print("   2. Cliquez sur 'Partager' en haut à droite")
        print("   3. Ajoutez cet email : sheet-writer@mail-agent-478513.iam.gserviceaccount.com")
        print("   4. Donnez les droits 'Éditeur'")
        print("   5. Relancez ce test")
        return False
    
    return True

def test_2_create_sheets():
    """Test 2 : Créer tous les onglets de catégories"""
    print("\n" + "="*70)
    print("TEST 2 : CRÉATION DES ONGLETS DE CATÉGORIES")
    print("="*70)
    
    result = create_all_category_sheets()
    
    if not result:
        print("\n❌ ÉCHEC : Impossible de créer les onglets")
        print("\n💡 SUGGESTION : Lancez d'abord le script d'initialisation :")
        print("   python init_spreadsheet.py")
        return False
    
    return True

def test_3_write_single_ticket():
    """Test 3 : Écrire un ticket de test"""
    print("\n" + "="*70)
    print("TEST 3 : ÉCRITURE D'UN TICKET UNIQUE")
    print("="*70)
    
    ticket = {
        "subject": "Test - Connexion impossible au serveur",
        "category": "Problème technique informatique",
        "urgency": "Élevée",
        "summary": "L'utilisateur ne peut pas se connecter au serveur depuis ce matin. Message d'erreur 'Connection timeout'."
    }
    
    print(f"\n📝 Ticket à écrire :")
    print(f"   Sujet : {ticket['subject']}")
    print(f"   Catégorie : {ticket['category']}")
    print(f"   Urgence : {ticket['urgency']}")
    print(f"   Résumé : {ticket['summary'][:60]}...")
    
    result = write_ticket(ticket)
    
    if not result:
        print("\n❌ ÉCHEC : Impossible d'écrire le ticket")
        return False
    
    return True

def test_4_write_multiple_tickets():
    """Test 4 : Écrire plusieurs tickets dans différentes catégories"""
    print("\n" + "="*70)
    print("TEST 4 : ÉCRITURE DE TICKETS DANS TOUTES LES CATÉGORIES")
    print("="*70)
    
    test_tickets = [
        {
            "subject": "Écran bleu au démarrage",
            "category": "Problème technique informatique",
            "urgency": "Critique",
            "summary": "Ordinateur affiche un écran bleu de la mort au démarrage. Travail urgent bloqué."
        },
        {
            "subject": "Demande de validation de congés",
            "category": "Demande administrative",
            "urgency": "Faible",
            "summary": "L'employé demande la validation de 2 semaines de congés pour le mois de juillet."
        },
        {
            "subject": "Réinitialisation de mot de passe",
            "category": "Problème d'accès / authentification",
            "urgency": "Modérée",
            "summary": "L'utilisateur a oublié son mot de passe et ne peut plus accéder à son compte."
        },
        {
            "subject": "Comment créer un rapport mensuel ?",
            "category": "Demande de support utilisateur",
            "urgency": "Anodine",
            "summary": "L'utilisateur demande une procédure détaillée pour générer les rapports mensuels."
        },
        {
            "subject": "Erreur 404 sur la page produits",
            "category": "Bug ou dysfonctionnement d'un service",
            "urgency": "Élevée",
            "summary": "La page produits retourne une erreur 404. Les clients ne peuvent pas consulter le catalogue."
        }
    ]
    
    success_count = 0
    for i, ticket in enumerate(test_tickets, 1):
        print(f"\n📝 Ticket {i}/{len(test_tickets)} : {ticket['category']}")
        result = write_ticket(ticket)
        if result:
            success_count += 1
    
    print(f"\n📊 Résultat : {success_count}/{len(test_tickets)} tickets écrits avec succès")
    
    return success_count == len(test_tickets)

def run_all_tests():
    """Exécute tous les tests dans l'ordre"""
    print("\n" + "🧪"*35)
    print("TESTS D'ÉCRITURE GOOGLE SHEETS")
    print("🧪"*35)
    
    tests = [
        ("Connexion au spreadsheet", test_1_connection),
        ("Création des onglets", test_2_create_sheets),
        ("Écriture d'un ticket", test_3_write_single_ticket),
        ("Écriture multiple", test_4_write_multiple_tickets)
    ]
    
    results = {}
    
    for test_name, test_func in tests:
        try:
            results[test_name] = test_func()
            
            # Si un test critique échoue, on arrête
            if not results[test_name] and test_name == "Connexion au spreadsheet":
                print("\n⚠️  Le test de connexion a échoué. Les autres tests sont annulés.")
                break
                
        except Exception as e:
            print(f"\n❌ Exception dans le test '{test_name}' : {e}")
            results[test_name] = False
    
    # Résumé final
    print("\n" + "="*70)
    print("RÉSUMÉ DES TESTS")
    print("="*70)
    
    for test_name, result in results.items():
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{status} - {test_name}")
    
    all_passed = all(results.values())
    
    print("\n" + "="*70)
    if all_passed:
        print("🎉 TOUS LES TESTS SONT PASSÉS !")
        print("\n✅ Votre système d'écriture Google Sheets fonctionne correctement.")
        print("✅ Vous pouvez maintenant lancer main.py pour traiter tous les emails.")
    else:
        print("⚠️  CERTAINS TESTS ONT ÉCHOUÉ")
        print("\n🔧 Vérifiez les erreurs ci-dessus et corrigez-les avant de continuer.")
    print("="*70)

if __name__ == "__main__":
    run_all_tests()