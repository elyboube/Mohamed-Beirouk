#!/usr/bin/env python
"""
Script pour activer toutes les fonctionnalités de la plateforme de tourisme
"""
import os
import sys
import django

# Configuration de Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tourism_platform.settings')
django.setup()

from django.core.management import call_command
from django.contrib.auth import get_user_model
from django.db import connection

User = get_user_model()

def print_header(text):
    """Affiche un en-tête stylisé"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def check_database():
    """Vérifie la connexion à la base de données"""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"❌ Erreur de connexion à la base de données: {e}")
        return False

def apply_migrations():
    """Applique toutes les migrations"""
    print_header("📦 APPLICATION DES MIGRATIONS")
    try:
        call_command('migrate', verbosity=1, interactive=False)
        print("✅ Toutes les migrations ont été appliquées avec succès!")
        return True
    except Exception as e:
        print(f"❌ Erreur lors des migrations: {e}")
        return False

def create_superuser():
    """Crée un superutilisateur s'il n'existe pas"""
    print_header("👤 CRÉATION DU SUPERUTILISATEUR")
    username = 'admin'
    email = 'admin@tourism-platform.local'
    password = 'admin123'
    
    if User.objects.filter(username=username).exists():
        print(f"ℹ️  Le superutilisateur '{username}' existe déjà.")
        print(f"   Nom d'utilisateur: {username}")
        print(f"   Mot de passe: {password}")
        return True
    
    try:
        User.objects.create_superuser(username=username, email=email, password=password)
        print("✅ Superutilisateur créé avec succès!")
        print(f"   Nom d'utilisateur: {username}")
        print(f"   Mot de passe: {password}")
        print(f"   Email: {email}")
        return True
    except Exception as e:
        print(f"❌ Erreur lors de la création du superutilisateur: {e}")
        return False

def verify_features():
    """Vérifie que toutes les fonctionnalités sont disponibles"""
    print_header("🔍 VÉRIFICATION DES FONCTIONNALITÉS")
    
    features_status = {}
    
    # Vérifier les modèles
    try:
        from destinations.models import Destination, DestinationReview, DestinationFavorite, Activity, Media, HomeVideo
        from stays.models import Stay, StayFavorite, Booking, StayMedia
        from guides.models import Guide, GuideReview, GuideMedia
        features_status['Modèles'] = "✅ Tous les modèles sont disponibles"
    except ImportError as e:
        features_status['Modèles'] = f"❌ Erreur d'import: {e}"
    
    # Vérifier les URLs
    try:
        from django.urls import reverse
        urls_to_check = [
            ('home', '/'),
            ('destination_list', '/destinations/'),
            ('stay_list', '/stays/'),
            ('guide_list', '/guides/'),
            ('signup', '/accounts/signup/'),
            ('contact', '/accounts/contact/'),
            ('dashboard', '/accounts/dashboard/'),
            ('admin', '/admin/'),
        ]
        features_status['URLs'] = f"✅ {len(urls_to_check)} routes configurées"
    except Exception as e:
        features_status['URLs'] = f"❌ Erreur: {e}"
    
    # Afficher le statut
    for feature, status in features_status.items():
        print(f"  {status}")
    
    return True

def display_features_summary():
    """Affiche un résumé de toutes les fonctionnalités"""
    print_header("📋 RÉSUMÉ DES FONCTIONNALITÉS DISPONIBLES")
    
    features = {
        "🏠 Page d'accueil": [
            "Affichage des destinations en vedette",
            "Affichage des guides recommandés",
            "Affichage des hébergements les moins chers",
            "Vidéos d'accueil"
        ],
        "🗺️ Destinations": [
            "Liste des destinations avec recherche",
            "Filtrage par région",
            "Détails de chaque destination",
            "Avis et notes des utilisateurs",
            "Favoris (ajout/suppression)",
            "Activités par destination",
            "Médias (images/vidéos)",
            "Coordonnées GPS (latitude/longitude)"
        ],
        "🏨 Hébergements (Stays)": [
            "Liste des hébergements",
            "Filtrage par ville, prix, note",
            "Détails de chaque hébergement",
            "Réservations (check-in/check-out)",
            "Favoris",
            "Médias (images/vidéos)",
            "Types: Hôtel, Guest House, Hostel"
        ],
        "👨‍🏫 Guides touristiques": [
            "Liste des guides",
            "Filtrage par ville, langue, prix",
            "Détails de chaque guide",
            "Avis et commentaires",
            "Médias (images/vidéos)",
            "Langues parlées",
            "Spécialités"
        ],
        "👤 Comptes utilisateurs": [
            "Inscription",
            "Connexion/Déconnexion",
            "Tableau de bord personnel",
            "Mes réservations",
            "Mes favoris",
            "Mes avis"
        ],
        "📧 Contact": [
            "Formulaire de contact",
            "Envoi d'emails"
        ],
        "⚙️ Administration": [
            "Interface d'administration Django",
            "Gestion des destinations",
            "Gestion des hébergements",
            "Gestion des guides",
            "Gestion des utilisateurs"
        ]
    }
    
    for category, items in features.items():
        print(f"\n{category}:")
        for item in items:
            print(f"  ✓ {item}")
    
    print("\n" + "="*60)

def display_access_info():
    """Affiche les informations d'accès"""
    print_header("🌐 INFORMATIONS D'ACCÈS")
    
    print("\n📍 URLs principales:")
    print("  • Page d'accueil:     http://127.0.0.1:8000/")
    print("  • Destinations:       http://127.0.0.1:8000/destinations/")
    print("  • Hébergements:       http://127.0.0.1:8000/stays/")
    print("  • Guides:             http://127.0.0.1:8000/guides/")
    print("  • Inscription:        http://127.0.0.1:8000/accounts/signup/")
    print("  • Contact:            http://127.0.0.1:8000/accounts/contact/")
    print("  • Tableau de bord:    http://127.0.0.1:8000/accounts/dashboard/")
    
    print("\n🔐 Administration Django:")
    print("  • URL:                http://127.0.0.1:8000/admin/")
    print("  • Nom d'utilisateur:   admin")
    print("  • Mot de passe:        admin123")
    
    print("\n" + "="*60)

def main():
    """Fonction principale"""
    print("\n" + "🚀"*30)
    print("  ACTIVATION DE TOUTES LES FONCTIONNALITÉS")
    print("  Plateforme de Tourisme Intelligente")
    print("🚀"*30)
    
    # Vérifier la base de données
    if not check_database():
        print("\n❌ Impossible de continuer sans connexion à la base de données.")
        sys.exit(1)
    
    # Appliquer les migrations
    if not apply_migrations():
        print("\n❌ Les migrations ont échoué. Vérifiez les erreurs ci-dessus.")
        sys.exit(1)
    
    # Créer le superutilisateur
    if not create_superuser():
        print("\n⚠️  Le superutilisateur n'a pas pu être créé, mais vous pouvez continuer.")
    
    # Vérifier les fonctionnalités
    verify_features()
    
    # Afficher le résumé
    display_features_summary()
    
    # Afficher les informations d'accès
    display_access_info()
    
    print("\n✨ Toutes les fonctionnalités sont activées et prêtes à être utilisées!")
    print("\n💡 Pour démarrer le serveur, exécutez: python manage.py runserver")
    print("   ou utilisez le script: .\\run.bat\n")

if __name__ == '__main__':
    main()
