import glob
import os
import sqlite3

# Chemin vers les fichiers de la base de données Kismet
db_path = '*.kismet'
list_of_files = glob.glob(db_path)
latest_file = max(list_of_files, key=os.path.getctime)
con_kismet = sqlite3.connect(latest_file)
cursor_kismet = con_kismet.cursor() 

# Connexion à la base de données 'cyt'
con_cyt = sqlite3.connect('cyt.db') 
cursor_cyt = con_cyt.cursor()

# Requête pour obtenir les données nécessaires de la table 'devices'
cursor_kismet.execute('SELECT last_time, devkey, devmac, type FROM devices')

# Itération sur chaque ligne de résultat
for row in cursor_kismet.fetchall():
    last_time, devkey, devmac, dev_type = row

    # Insertion des données dans la table 'time_presence' de 'cyt'
    cursor_cyt.execute('INSERT INTO time_presence (first_time_since_cyt_launched, mac_address) VALUES (?, ?)', (last_time, devmac))

    # Insertion des données dans la table 'devices' de 'cyt'
    cursor_cyt.execute('INSERT INTO devices (device_key, type_of_connection, mac_address) VALUES (?, ?, ?)', (devkey, dev_type, devmac))

# Validation des modifications
con_cyt.commit()

# Fermeture des connexions
con_kismet.close()
con_cyt.close()
