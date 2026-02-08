import mysql.connector
from mysql.connector import errorcode

# --- 1. DÉFINITION DU PLAN (LES TABLES) ---
DB_NAME = 'movie_recommendation'
TABLES = {}

# Table pour les films (ID, Titre, Genres)
TABLES['movies'] = (
    "CREATE TABLE `movies` ("
    "  `movieId` int NOT NULL,"
    "  `title` varchar(255) NOT NULL,"
    "  `genres` varchar(255),"
    "  PRIMARY KEY (`movieId`)"
    ") ENGINE=InnoDB")

# Table pour les notes (Utilisateur, Film, Note, Date)
TABLES['ratings'] = (
    "CREATE TABLE `ratings` ("
    "  `userId` int NOT NULL,"
    "  `movieId` int NOT NULL,"
    "  `rating` float NOT NULL,"
    "  `timestamp` int,"
    "  FOREIGN KEY (`movieId`) REFERENCES `movies` (`movieId`)"
    ") ENGINE=InnoDB")

# --- 2. CONFIGURATION DE LA CONNEXION ---
config = {
    'user': 'root',
    'password': '23INP01027@c',  # Ton mot de passe
    'host': 'localhost',
    'port': 2004                 # Ton port Docker (externe)
}

# --- 3. FONCTION DE CRÉATION DE LA BASE ---
def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"✅ Base de données '{DB_NAME}' créée avec succès.")
    except mysql.connector.Error as err:
        print(f"❌ Erreur lors de la création de la DB : {err}")
        exit(1)

# --- 4. EXÉCUTION PRINCIPALE ---
try:
    # Connexion au serveur MySQL
    print("🔌 Connexion au serveur MySQL...")
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Sélection ou Création de la Base de Données
    try:
        cursor.execute(f"USE {DB_NAME}")
        print(f"📂 Base de données '{DB_NAME}' sélectionnée.")
    except mysql.connector.Error as err:
        print(f"⚠️ La base '{DB_NAME}' n'existe pas.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # Création des Tables (Boucle)
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"🔨 Création de la table '{table_name}'...", end='')
            cursor.execute(table_description)
            print(" FAIT !")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(" DÉJÀ EXISTANTE.")
            else:
                print(f"\n❌ Erreur SQL : {err.msg}")

    # Fermeture propre
    cursor.close()
    cnx.close()
    print("\n🚀 SUCCÈS : L'infrastructure de données est prête !")

except mysql.connector.Error as err:
    print(f"❌ Erreur de connexion : {err}")