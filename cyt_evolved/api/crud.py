import db as database
import schema as schema

def addADevice(db, mac_address):
    try:
        new_whitelisted_device = database.Whitelist(mac_address=mac_address)
        db.add(new_whitelisted_device)
        db.commit()
    except:
        return False 
    return True

def addDetectedDevice(db):
    try:
        devices = db.query(database.Devices).all()
        for item in devices:
            new_whitelisted_device = database.Whitelist(mac_address = item.mac_address)
            db.add(new_whitelisted_device)
        db.commit()
    except:
        return False
    return True

def addActuallyDetectedDevice(db):
    try:
        devices = db.query(database.TimePresence).filter(
                (database.TimePresence.zero_to_five != False) |
                (database.TimePresence.five_to_ten != False) |
                (database.TimePresence.ten_to_fifteen != False) |
                (database.TimePresence.fifteen_to_twenty != False) |
                (database.TimePresence.twenty_and_more != False)
            ).all()
        for item in devices:
            new_whitelisted_device = database.Whitelist(mac_address = item.mac_address)
            db.add(new_whitelisted_device)
        db.commit()
    except:
        return False
    return True

def deleteADevice(db, mac_address):
    try:
        unwhitelisted_device = db.query(database.Whitelist).filter(database.Whitelist.mac_address == mac_address).first()
        db.delete(unwhitelisted_device)
        db.commit()
    except:
        return False 
    return True

def getWhitelist(db):
    return db.query(database.Whitelist).all()

def deleteAllDevices(db):
    try:
        unwhitelisted_devices = db.query(database.Whitelist).all()
        for device in unwhitelisted_devices:
            db.delete(device)
        db.commit()
    except:
        return False 
    return True

def getDetectedDevices(db):
    return db.query(database.Devices).all()

def getActuallyDetectedDevices(db):
    return db.query(database.TimePresence).filter(
        (database.TimePresence.zero_to_five != False) |
        (database.TimePresence.five_to_ten != False) |
        (database.TimePresence.ten_to_fifteen != False) |
        (database.TimePresence.fifteen_to_twenty != False) |
        (database.TimePresence.twenty_and_more != False)
    ).all()

def get_0To5DetectedDevices(db):
    return db.query(database.TimePresence).filter(
        (database.TimePresence.zero_to_five != False)
    ).all()

def get_5To10DetectedDevices(db):
    return db.query(database.TimePresence).filter(
        (database.TimePresence.five_to_ten != False)
    ).all()

def get_10To15DetectedDevices(db):
    return db.query(database.TimePresence).filter(
        (database.TimePresence.ten_to_fifteen != False)
    ).all()

def get_15To20DetectedDevices(db):
    return db.query(database.TimePresence).filter(
        (database.TimePresence.fifteen_to_twenty != False)
    ).all()

def get_20AndMoreDetectedDevices(db):
    return db.query(database.TimePresence).filter(
        (database.TimePresence.twenty_and_more != False)
    ).all()

