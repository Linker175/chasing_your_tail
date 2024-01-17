import sqlite3

# Fonction pour créer la base de données et les tables
def create_database_and_tables():
    # Connexion à la base de données (elle sera créée si elle n'existe pas encore)
    conn = sqlite3.connect("cyt.db")

    # Création d'un curseur pour exécuter des commandes SQL
    cursor = conn.cursor()

    # Création de la table "devices"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS devices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_key TEXT,
        mac_address TEXT,
        type_of_connection TEXT
    )
    """)

    # Création de la table "time_presence"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS time_presence (
        mac_address TEXT,
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_time_since_cyt_launched INTEGER,
        last_time_since_cyt_launched INTEGER,
        zero_to_five BOOLEAN DEFAULT 0,
        five_to_ten BOOLEAN DEFAULT 0,
        ten_to_fifteen BOOLEAN DEFAULT 0,
        fifteen_to_twenty BOOLEAN DEFAULT 0,
        twenty_and_more BOOLEAN DEFAULT 0
    )
    """)

    # Création de la table "whitelist"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS whitelist (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        mac_address TEXT
    )
    """)

    # Enregistrement des modifications et fermeture de la connexion
    conn.commit()
    conn.close()

# Appel de la fonction pour créer la base de données et les tables
create_database_and_tables()

print("Base de données 'cyt' créée avec succès.")
