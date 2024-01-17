import glob
import os
import sqlite3
import datetime
import subprocess


#Path to kismet db file (taking the last one)
db_path = '*.kismet'
list_of_files = glob.glob(db_path)
latest_file = max(list_of_files, key=os.path.getctime)
con_kismet = sqlite3.connect(latest_file)
cursor_kismet = con_kismet.cursor() 

#Change of DB file
old_file_name = "cyt.db"
new_file_name = f"cyt_{datetime.now().strftime('%Y-%m-%d-%H:%M')}.db"
os.rename(old_file_name, new_file_name)

subprocess.run(["create_database.py"])

con_cyt = sqlite3.connect('cyt.db') 
cursor_cyt = con_cyt.cursor()

#Store the actual time into a file
timestamp = int((datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
time_storage_file = "timestamp_storage"

with open(time_storage_file, "w") as file:
    file.write(str(timestamp))

#Request to get the necessary data
cursor_kismet.execute('SELECT last_time, devkey, devmac, type FROM devices')

# Itération sur chaque ligne de résultat
for row in cursor_kismet.fetchall():
    last_time, devkey, devmac, dev_type = row

    if last_time > timestamp:
        # Insertion des données dans la table 'time_presence' de 'cyt'
        cursor_cyt.execute('INSERT INTO time_presence (first_time_since_cyt_launched, mac_address) VALUES (?, ?)', (last_time, devmac))

        # Insertion des données dans la table 'devices' de 'cyt'
        cursor_cyt.execute('INSERT INTO devices (device_key, type_of_connection, mac_address) VALUES (?, ?, ?)', (devkey, dev_type, devmac))

# Validation des modifications
con_cyt.commit()

# Fermeture des connexions
con_kismet.close()
con_cyt.close()
