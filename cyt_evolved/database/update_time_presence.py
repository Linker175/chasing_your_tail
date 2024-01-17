import sqlite3
from datetime import datetime

def difference_between_now_and_given_epoch(epoch_timestamp):
    datetime_obj = datetime.utcfromtimestamp(epoch_timestamp)
    now = datetime.now()
    gap = now - datetime_obj
    seconds = gap.total_seconds()
    return seconds/60

def difference_between_two_epoch(epoch_one, epoch_two):
    datetime_obj = datetime.utcfromtimestamp(epoch_one)
    datetime_obj2 = datetime.utcfromtimestamp(epoch_two)
    gap = datetime_obj - datetime_obj2
    seconds = gap.total_seconds()
    return seconds/60

## ATTENTION IL PEUT Y AVOIR DES ERREUR AVEC LES FUSEAUX HORAIRES à vérifier

con_cyt = sqlite3.connect('cyt.db')
cursor_cyt = con_cyt.cursor()

cursor_cyt.execute('SELECT mac_address, first_time_since_cyt_launched, last_time_since_cyt_launched, zero_to_five, five_to_ten,ten_to_fifteen, fifteen_to_twenty, twenty_and_more type FROM time_presence')


for row in cursor_cyt.fetchall():
    mac_address, first_time_since_cyt_launched, last_time_since_cyt_launched, zero_to_five, five_to_ten,ten_to_fifteen, fifteen_to_twenty, twenty_and_more  = row
    if ((zero_to_five == False) and (five_to_ten == False) and (ten_to_fifteen == False) and (fifteen_to_twenty == False) and (twenty_and_more == False) and (difference_between_now_and_given_epoch(last_time_since_cyt_launched))<5):
        first_time_since_cyt_launched = last_time_since_cyt_launched
        zero_to_five = True
    if ((zero_to_five == True) and (difference_between_two_epoch(last_time_since_cyt_launched,first_time_since_cyt_launched) > 5)):
        zero_to_five = False
        five_to_ten = True
    if ((five_to_ten == True) and (difference_between_two_epoch(last_time_since_cyt_launched,first_time_since_cyt_launched) > 10)):
        five_to_ten = False
        ten_to_fifteen = True
    if ((ten_to_fifteen == True) and (difference_between_two_epoch(last_time_since_cyt_launched,first_time_since_cyt_launched) > 15)):
        ten_to_fifteen = False
        fifteen_to_twenty = True
    if ((fifteen_to_twenty == True) and (difference_between_two_epoch(last_time_since_cyt_launched,first_time_since_cyt_launched) > 20)):
        fifteen_to_twenty = False
        twenty_and_more = True
    if (((zero_to_five == True) or (five_to_ten == True) or (ten_to_fifteen == True) or (fifteen_to_twenty == True) or (twenty_and_more == True)) and (difference_between_now_and_given_epoch(last_time_since_cyt_launched)>5)):
        zero_to_five = False
        five_to_ten = False
        ten_to_fifteen = False
        fifteen_to_twenty = False
        twenty_and_more = False
    cursor_cyt.execute('UPDATE time_presence SET first_time_since_cyt_launched = ?, zero_to_five = ?, five_to_ten = ?, ten_to_fifteen = ?, fifteen_to_twenty = ?, twenty_and_more = ? WHERE mac_address = ?', (first_time_since_cyt_launched, zero_to_five, five_to_ten, ten_to_fifteen, fifteen_to_twenty, twenty_and_more, mac_address))
    con_cyt.commit()
con_cyt.close()
 

