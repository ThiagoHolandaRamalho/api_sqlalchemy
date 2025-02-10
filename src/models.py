from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from db import Base,engine


class Bilhetes(Base):
    __tablename__ = 'bilhetes_cyber'
    id = Column(Integer,primary_key=True, index=True)
    uuid = Column(String)
    uuidInstallments = Column(String)
    Plan = Column(String)
    name = Column(String)
    nameSocial= Column(String)
    cpf = Column(String)
    status = Column(String)
    quotecounter = Column(String)
    luckyNumber = Column(String)
    cotationDate = Column(String)
    expirationDate = Column(String)
    cancelMotivo= Column(String)
    cancelDate = Column(String)
    IdEndosso = Column(String)
    cdApolice = Column(String)
    ComissionFee = Column(String)
    TariffPrize = Column(String)
    FIF = Column(String)
    RenewalFrom = Column(String)
    UF = Column(String)
    created_at = Column(DateTime, default=func.now())  # Campo adicionado



class InstallmentsCyber(Base):
  
    __tablename__ = 'parcelas_cyber' 
    id = Column(Integer,primary_key=True, index=True)
    installmentDate = Column(String)
    installmentDueDate = Column(String)
    installmentStatus = Column(String)
    StatusDetail = Column(String)
    number = Column(String)
    chargeBack = Column(String)
    parcelValue = Column(String)
    transactionID = Column(String)
    chargeBackDate = Column(String)
    paymentDate = Column(String)
    uuidInstallments = Column(String)
    created_at = Column(DateTime, default=func.now())  # Campo adicionado



Base.metadata.create_all(engine)