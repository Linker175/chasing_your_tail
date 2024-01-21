import glob
import os
import sqlite3

# Chemin vers les fichiers de la base de données Kismet
db_path = '/home/pi/Desktop/chasing_your_tail/kismet_logs/*.kismet'
db_path = os.path.expanduser(db_path)
list_of_files = glob.glob(db_path)
latest_file = max(list_of_files, key=os.path.getctime)
con_kismet = sqlite3.connect(latest_file)
cursor_kismet = con_kismet.cursor()

# Connexion à la base de données 'cyt'
con_cyt = sqlite3.connect('/home/pi/Desktop/chasing_your_tail/cyt_evolved/database/cyt.db')
cursor_cyt = con_cyt.cursor()

# Requête pour obtenir les données nécessaires de la table 'devices'
cursor_kismet.execute('SELECT last_time, devkey, devmac, type FROM devices')

#We get back timestamp
timestamp_file_storage = "/home/pi/Desktop/chasing_your_tail/cyt_evolved/database/timestamp_storage"

with open(timestamp_file_storage, "r") as file:
    content = file.read()

timestamp = int(content) 

# Itération sur chaque ligne de résultat
for row in cursor_kismet.fetchall():
    last_time, devkey, devmac, dev_type = row

    if timestamp < last_time:
        # Vérifier si devmac est déjà présent dans la table 'time_presence' de 'cyt'
        cursor_cyt.execute('SELECT COUNT(*) FROM time_presence WHERE mac_address = ?', (devmac, ))
        if cursor_cyt.fetchone()[0] > 0:
            # Mise à jour de 'last_time_since_cyt_launched' si devmac est trouvé
            cursor_cyt.execute('UPDATE time_presence SET last_time_since_cyt_launched = ? WHERE mac_address = ?', (last_time, devmac))
        else:
            # Insertion des données si devmac n'est pas trouvé
            cursor_cyt.execute('INSERT INTO time_presence (first_time_since_cyt_launched, last_time_since_cyt_launched, mac_address) VALUES (?, ?, ?)', (last_time, last_time, devmac))
            cursor_cyt.execute('INSERT INTO devices (device_key, type_of_connection, mac_address) VALUES (?, ?, ?)', (devkey, dev_type, devmac))
            
# Validation des modifications
con_cyt.commit()

# Fermeture des connexions
con_kismet.close()
con_cyt.close()
