import mysql.connector

# --- EXPLICATION DU CODE ---
# 1. On configure l'adresse de la base de données
config = {
    'user': 'root',
    'password': '23INP01027@c',  # Le mot de passe défini dans Docker
    'host': 'localhost',     # C'est ton ordinateur
    'port': '2004',      # IMPORTANT : Le port externe vu dans docker ps
    'database': 'sys'        # Une base système qui existe toujours
}

print("🔌 Tentative de connexion au port 2004...")

try:
    # 2. On essaie d'ouvrir la porte
    conn = mysql.connector.connect(**config)
    
    if conn.is_connected():
        print("✅ SUCCÈS ! La connexion est réussie.")
        print(f"Version du serveur MySQL : {conn.get_server_info()}")
        
        # 3. On referme la porte proprement
        conn.close()

except Exception as erreur:
    print(f"❌ ÉCHEC : {erreur}")