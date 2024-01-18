import glob
import os
import sqlite3
import datetime
import subprocess


#Path to kismet db file (taking the last one)
db_path = '../../kismet_logs/*.kismet'
list_of_files = glob.glob(db_path)
latest_file = max(list_of_files, key=os.path.getctime)
con_kismet = sqlite3.connect(latest_file)
cursor_kismet = con_kismet.cursor() 

#Change of DB file
old_file_name = "../database/cyt.db"
if os.path.isfile(old_file_name):
    new_file_name = f"../database/cyt_{datetime.datetime.now().strftime('%Y-%m-%d-%H:%M')}.db"
    os.rename(old_file_name, new_file_name)

path_to_create_db = "../database/create_database.py"
subprocess.run(["python", path_to_create_db])


#Use the DB file
con_cyt = sqlite3.connect('../database/cyt.db') 
cursor_cyt = con_cyt.cursor()

#Store the actual time into a file
timestamp = int((datetime.datetime.now() - datetime.datetime(1970, 1, 1)).total_seconds())
time_storage_file = "../database/timestamp_storage"

with open(time_storage_file, "w") as file:
    file.write(str(timestamp))

#Request to get the necessary data
cursor_kismet.execute('SELECT last_time, devkey, devmac, type FROM devices')

#Iteration on each line of the db
for row in cursor_kismet.fetchall():
    last_time, devkey, devmac, dev_type = row

    #We only take the values that are since the last scan
    if last_time > timestamp:
        #Data insertion in table 'time_presence' of 'cyt'
        cursor_cyt.execute('INSERT INTO time_presence (first_time_since_cyt_launched, mac_address) VALUES (?, ?)', (last_time, devmac))

        #Data insertion in table 'devices' of 'cyt'
        cursor_cyt.execute('INSERT INTO devices (device_key, type_of_connection, mac_address) VALUES (?, ?, ?)', (devkey, dev_type, devmac))

#Validation of modifications
con_cyt.commit()

#Connexion close
con_kismet.close()
con_cyt.close()
