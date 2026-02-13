import os
from dotenv import load_dotenv
import mysql.connector
from mysql.connector import errorcode

# Load environment variables from .env file
load_dotenv()

# --- CONFIGURATION ---
DB_NAME = os.getenv('MYSQL_DATABASE', 'movie_recommendation')
config = {
    'user': 'root',
    'password': os.getenv('MYSQL_ROOT_PASSWORD'),
    'host': os.getenv('MYSQL_HOST', 'localhost'),
    'port': int(os.getenv('MYSQL_PORT', 2004))
}

# 1. Table definition: MOVIES (Catalog)
TABLES = {}
TABLES['movies'] = (
    "CREATE TABLE `movies` ("
    "  `movieId` int NOT NULL,"
    "  `title` varchar(255) NOT NULL,"
    "  `genres` varchar(255),"
    "  PRIMARY KEY (`movieId`)"
    ") ENGINE=InnoDB")

# 2. Table definition: RATINGS (Interactions)
TABLES['ratings'] = (
    "CREATE TABLE `ratings` ("
    "  `userId` int NOT NULL,"
    "  `movieId` int NOT NULL,"
    "  `rating` float NOT NULL,"
    "  `timestamp` int,"
    "  FOREIGN KEY (`movieId`) REFERENCES `movies` (`movieId`)"
    ") ENGINE=InnoDB")

def create_database(cursor):
    try:
        cursor.execute(f"CREATE DATABASE {DB_NAME} DEFAULT CHARACTER SET 'utf8'")
        print(f"✅ Database '{DB_NAME}' created successfully.")
    except mysql.connector.Error as err:
        print(f"❌ Failed creating database: {err}")
        exit(1)

# --- MAIN EXECUTION ---
try:
    # Connect to MySQL Server
    print("🔌 Connecting to MySQL server...")
    cnx = mysql.connector.connect(**config)
    cursor = cnx.cursor()

    # Select or Create Database
    try:
        cursor.execute(f"USE {DB_NAME}")
        print(f"📂 Database '{DB_NAME}' selected.")
    except mysql.connector.Error as err:
        print(f"⚠️ Database '{DB_NAME}' does not exist.")
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            cnx.database = DB_NAME
        else:
            print(err)
            exit(1)

    # Create Tables
    for table_name in TABLES:
        table_description = TABLES[table_name]
        try:
            print(f"🔨 Creating table '{table_name}'...", end='')
            cursor.execute(table_description)
            print(" DONE!")
        except mysql.connector.Error as err:
            if err.errno == errorcode.ER_TABLE_EXISTS_ERROR:
                print(" ALREADY EXISTS.")
            else:
                print(f"\n❌ SQL Error: {err.msg}")

    # Clean exit
    cursor.close()
    cnx.close()
    print("\n🚀 SUCCESS: Data infrastructure is ready!")

except mysql.connector.Error as err:
    print(f"❌ Connection Error: {err}")