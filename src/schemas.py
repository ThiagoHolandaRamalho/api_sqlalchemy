from pydantic import BaseModel
from typing import List, Optional


class SchemaBilheteCyber(BaseModel):
    uuid: str
    uuidInstallments : str
    Plan : str
    name : str
    nameSocial: str
    cpf : str
    status : str
    quotecounter : str
    luckyNumber : str
    cotationDate : str
    expirationDate : str
    cancelMotivo: str
    cancelDate:str
    IdEndosso : str
    cdApolice :str
    ComissionFee : str
    TariffPrize : str
    FIF:str
    RenewalFrom:str
    UF:str

    class Config:
        orm = True


class SchemaInstallmentCyber(BaseModel):
    installmentDate: str
    installmentDueDate: str 
    installmentStatus: str  
    StatusDetail: str  
    number: str 
    chargeBack: str
    parcelValue: str 
    transactionID: str 
    chargeBackDate: str
    paymentDate: str
    uuidInstallments: str  

    class Config:
        orm = True

if __name__ == '__main__':
    ...