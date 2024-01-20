from fastapi import Depends, FastAPI, Body, Query
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from typing import Annotated
import db as db
import schema as schema
import crud as crud
import subprocess

from fastapi import FastAPI, APIRouter

db.Base.metadata.create_all(bind=db.engine)

app = FastAPI()

#Endpoint for Scan
router_scan = APIRouter(tags=["Scan"])


@router_scan.get("/scan/launch/", response_model=schema.Scan)
def launchScan(
):  
    path_to_scan = "../database/first_fill_database.py"
    try:
        db.close_all_sessions()
        subprocess.run(["python", path_to_scan])
    except Exception as e:
        print(str(e))
        return {"scanLaunchSuccess":False}
    return {"scanLaunchSuccess":True}


app.include_router(router_scan)



#Endpoint for Whitelist 
router_whitelist = APIRouter(tags=["Whitelist"])

@router_whitelist.get("/whitelist/getWhitelist/", response_model=schema.Device)
def listDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.getWhitelist(db=db)
    return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})

@router_whitelist.post("/whitelist/addADevice/", response_model=schema.Upload)
def addADevice(
    payload: schema.MacAddress,
    db: Session = Depends(db.get_db)
):
    if not crud.addADevice(db=db, mac_address=payload.macAddress):
            return {"uploadSuccess": False}
    return {"uploadSuccess": True}

@router_whitelist.post("/whitelist/addDetectedDevices/", response_model=schema.Upload)
def addDetectedDevices(
    db: Session = Depends(db.get_db)
):
    if not crud.addDetectedDevice(db=db):
            return {"uploadSuccess": False}
    return {"uploadSuccess": True}

@router_whitelist.post("/whitelist/addActuallyDetectedDevices/", response_model=schema.Upload)
def addActuallyDetectedDevices(
    db: Session = Depends(db.get_db)
):
    if not crud.addActuallyDetectedDevice(db=db):
            return {"uploadSuccess": False}
    return {"uploadSuccess": True}

@router_whitelist.post("/whitelist/deleteADevice/", response_model=schema.Delete)
def deleteADevice( 
    payload: schema.MacAddress,
    db: Session = Depends(db.get_db)
):
    if not crud.deleteADevice(db=db, mac_address=payload.macAddress):
            return {"deleteSuccess": False}
    return {"deleteSuccess": True}

@router_whitelist.post("/whitelist/deleteAllDevices/", response_model=schema.Delete)
def deleteAllDevices(
    db: Session = Depends(db.get_db)
):
    if not crud.deleteAllDevices(db=db):
            return {"deleteSuccess": False}
    return {"deleteSuccess": True}

app.include_router(router_whitelist)

#Endpoint for detected devices 
router_devices = APIRouter(tags=["Detected Devices"])

@router_devices.get("/devices/getDetectedDevices/", response_model=schema.Device)
def getDetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.getDetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

@router_devices.get("/devices/getActuallyDetectedDevices/", response_model=schema.Device)
def getActuallyDetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.getActuallyDetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

@router_devices.get("/devices/get0To5DetectedDevices/", response_model=schema.Device)
def get0To5DetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.get_0To5DetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

app.include_router(router_devices)

@router_devices.get("/devices/get5To10DetectedDevices/", response_model=schema.Device)
def get5To10DetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.get_5To10DetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

@router_devices.get("/devices/get10To15DetectedDevices/", response_model=schema.Device)
def get10To15DetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.get_10To15DetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

app.include_router(router_devices)

@router_devices.get("/devices/get15To20DetectedDevices/", response_model=schema.Device)
def get15To20DetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.get_15To20DetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

app.include_router(router_devices)

@router_devices.get("/devices/get20AndMoreDetectedDevices/", response_model=schema.Device)
def get20AndMoreDetectedDevices(
    db: Session = Depends(db.get_db)
):
    data = crud.get_20AndMoreDetectedDevices(db=db)
    data_whitelisted = crud.getWhitelist(db=db) 
    if len(data_whitelisted) == 0:
        return schema.Device(macAddresses={entry.id: entry.mac_address for entry in data})
    macAddresses={}
    for entry in data:
        pass_this_round = 0
        for entry2 in data_whitelisted:
            if entry2.mac_address == entry.mac_address:
                pass_this_round = 1
        if pass_this_round == 0:
            macAddresses.update({entry.id: entry.mac_address})
    return schema.Device(macAddresses=macAddresses)

app.include_router(router_devices)
