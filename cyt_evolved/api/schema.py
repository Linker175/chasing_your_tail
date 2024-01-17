from pydantic import BaseModel, Field, validator
import re

class Scan(BaseModel):
    scanLaunchSuccess:bool

class Upload(BaseModel):
    uploadSuccess: bool      

class Delete(BaseModel):
    deleteSuccess: bool   

class Empty(BaseModel):
    empty: bool

class Device(BaseModel):
    macAddresses : dict[int,str] = Field(..., example={"1":"00:1A:2B:3C:4D:5E", "2":"00:1A:2B:3C:4D:5E", "...":"..."})   

class MacAddress(BaseModel):
    macAddress: str = Field(..., example="00:1A:2B:3C:4D:5E")

    @validator('macAddress')
    def validate_mac_address(cls, v):
        if re.match("[0-9a-fA-F]{2}([-:])[0-9a-fA-F]{2}(\\1[0-9a-fA-F]{2}){4}$", v):
            return v
        raise ValueError('Invalid MAC address format')

 