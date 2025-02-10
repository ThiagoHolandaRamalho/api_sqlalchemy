import requests
#from db import SessionLocal, engine, Base
from models import Bilhetes , InstallmentsCyber
from schemas import SchemaBilheteCyber ,SchemaInstallmentCyber
import json
from db import abrir_sessao_sql_server
import time


from typing import Dict, List
from pydantic_core import ErrorDetails
from pydantic import BaseModel, HttpUrl, ValidationError


CUSTOM_MESSAGES = {
    'int_parsing': 'This is not an integer! 🤦',
    'url_scheme': 'Hey, use the right URL scheme! I wanted {expected_schemes}.',
}

def convert_errors(
    e: ValidationError, custom_messages: Dict[str, str]
) -> List[ErrorDetails]:
    new_errors: List[ErrorDetails] = []
    for error in e.errors():
        custom_message = custom_messages.get(error['type'])
        if custom_message:
            ctx = error.get('ctx')
            error['msg'] = (
                custom_message.format(**ctx) if ctx else custom_message
            )
        new_errors.append(error)
    return new_errors



TEMPO_SLEEP = 5
QDE_TENTATIVAS = 30
qde_loops = 0
qde_loops = 0


def buscar_bilhetes(bilhete:str|int) -> SchemaBilheteCyber:
    
    url = "https://consumer.kovr.com.br/apis/SearchPicpay"
    payload = json.dumps({
    "policyNumber": f"{bilhete}"
    })
    headers = {
    'Content-Type': 'application/json',
    }

    while True:
        try:
            response = requests.request("POST", url, headers=headers, data=payload,timeout=120)

            if response.status_code == 200:

                if not response:
                    return None

                dados = response.json()[0]
                return SchemaBilheteCyber(
                     uuid = dados.get('uuid')
                    ,uuidInstallments = dados.get('uuidInstallments')
                    ,Plan = dados.get('Plan')
                    ,name = dados.get('name')
                    ,nameSocial = dados.get('nameSocial')
                    ,cpf = dados.get('cpf')
                    ,status = dados.get('status')
                    ,quotecounter = dados.get('quotecounter')
                    ,luckyNumber = dados.get('luckyNumber')
                    ,cotationDate = dados.get('cotationDate')
                    ,expirationDate = dados.get('expirationDate')
                    ,cancelMotivo = dados.get('cancelMotivo')
                    ,cancelDate = dados.get('cancelDate')
                    ,IdEndosso = dados.get('IdEndosso')
                    ,cdApolice = dados.get('cdApolice')
                    ,ComissionFee = dados.get('ComissionFee')
                    ,TariffPrize= dados.get('TariffPrize')
                    ,FIF= dados.get('FIF')
                    ,RenewalFrom= dados.get('RenewalFrom')
                    ,UF= dados.get('UF')
                 )
                
            else:
                pass
        except ValidationError as e:
            errors = convert_errors(e, CUSTOM_MESSAGES)
            print(errors)
            raise  ' ++++++++++++++++++++++++ Erro de Contrato de dados ++++++++++++++++++++++++++++++++++'
        except:
            time.sleep(TEMPO_SLEEP)
            qde_loops += 1
            if qde_loops >QDE_TENTATIVAS:
                return None
            pass

def importar_bilhete(bilhete_schema: SchemaBilheteCyber) -> Bilhetes:

    engine,SessionLocal,base =  abrir_sessao_sql_server()

    with SessionLocal() as db:
        db_bilhete = Bilhetes(

         uuid = bilhete_schema.uuid
        ,uuidInstallments = bilhete_schema.uuidInstallments
        ,Plan = bilhete_schema.Plan
        ,name = bilhete_schema.name
        ,nameSocial = bilhete_schema.nameSocial
        ,cpf = bilhete_schema.cpf
        ,status = bilhete_schema.status
        ,quotecounter = bilhete_schema.quotecounter
        ,luckyNumber = bilhete_schema.luckyNumber
        ,cotationDate = bilhete_schema.cotationDate
        ,expirationDate = bilhete_schema.expirationDate
        ,cancelMotivo= bilhete_schema.cancelMotivo
        ,cancelDate = bilhete_schema.cancelDate
        ,IdEndosso = bilhete_schema.IdEndosso
        ,cdApolice = bilhete_schema.cdApolice
        ,ComissionFee = bilhete_schema.ComissionFee
        ,TariffPrize = bilhete_schema.TariffPrize
        ,FIF = bilhete_schema.FIF
        ,RenewalFrom = bilhete_schema.RenewalFrom
        ,UF = bilhete_schema.UF
        )
        
        db.add(db_bilhete)
        db.commit()
        db.refresh(db_bilhete)
    return db_bilhete


def filtrar_bilhete(bilhete: str) :
    engine,SessionLocal,base =  abrir_sessao_sql_server()
    with SessionLocal() as db:
        resultado = db.query(Bilhetes).filter(Bilhetes.quotecounter == f'{bilhete}').all()
        if resultado:
            for res in resultado:
                db.delete(res)
                db.commit()

    


def buscar_parcelas_cyber(uuid_intsallment:str):
    url = "https://consumer.kovr.com.br/apis/getInstallment"

    payload = json.dumps({
    "uuid": f"{uuid_intsallment}"
    })
    headers = {
    'Content-Type': 'application/json'
    }
    response = requests.request("POST", url, headers=headers, data=payload)

    if response.status_code == 200:
        dados = response.json()
        
        if dados.get('Installments') is None:
            return None

        uuidInstallment = dados.get('uuid')
        parcelas = dados.get('Installments')
        {parc.update({'uuidInstallments':uuidInstallment}) for parc in parcelas}

        lista_parcelas = []
        for parc in parcelas:
            parc_schema = SchemaInstallmentCyber(
                installmentDate = parc.get('installmentDate'),
                installmentDueDate = parc.get('installmentDueDate'), 
                installmentStatus = parc.get('installmentStatus'),  
                StatusDetail = parc.get('StatusDetail'),  
                number = parc.get('number'),
                chargeBack = parc.get('chargeBack'),
                parcelValue = parc.get('parcelValue'), 
                transactionID = parc.get('transactionID'), 
                chargeBackDate = parc.get('chargeBackDate'),
                paymentDate = parc.get('paymentDate'),
                uuidInstallments = parc.get('uuidInstallments')
            )
            lista_parcelas.append(parc_schema)
        return lista_parcelas
    else:
        return None
    




def importar_parcelas_bilhetes_cyber(bilhetes_schemas : list[SchemaInstallmentCyber]) -> InstallmentsCyber:
    engine,SessionLocal,base =  abrir_sessao_sql_server()
    inputs = []
    with SessionLocal() as db:

        for  bilhete_schema in bilhetes_schemas:
            db_parcelas_bilhete = InstallmentsCyber(
                    installmentDate = bilhete_schema.installmentDate,
                    installmentDueDate = bilhete_schema.installmentDueDate,
                    installmentStatus = bilhete_schema.installmentStatus,
                    StatusDetail = bilhete_schema.StatusDetail,
                    number = bilhete_schema.number,
                    chargeBack = bilhete_schema.chargeBack,
                    parcelValue = bilhete_schema.parcelValue,
                    transactionID = bilhete_schema.transactionID,
                    chargeBackDate = bilhete_schema.chargeBackDate,
                    paymentDate = bilhete_schema.paymentDate,
                    uuidInstallments = bilhete_schema.uuidInstallments
                    )
            inputs.append(db_parcelas_bilhete)
        
        db.add_all(inputs)
        db.commit()
        #db.refresh(inputs)
    return inputs

def filtrar_parcelas_bilhete(uuidIsntallment: str) :
    engine,SessionLocal,base =  abrir_sessao_sql_server()
    with SessionLocal() as db:
        resultado = db.query(InstallmentsCyber).filter(InstallmentsCyber.uuidInstallments == f'{uuidIsntallment}').all()
        if resultado:
            for res in resultado:
                db.delete(res)
                db.commit()


def importar_registros_cyber(new_bilhete):
   
    filtrar_bilhete(new_bilhete)
    dados = buscar_bilhetes(bilhete=new_bilhete)
    
    if dados:
        retornos  = importar_bilhete(dados)
       #print(f'Sucesso {new_bilhete}')
    
    if dados.uuidInstallments:
        filtrar_parcelas_bilhete(dados.uuidInstallments)
        retornos_parcelas =  buscar_parcelas_cyber(dados.uuidInstallments)
        
        if retornos_parcelas:
            importar_parcelas_bilhetes_cyber(retornos_parcelas)


if __name__ =='__main__':

    d = filtrar_bilhete(bilhete=171164750)
    if d:
        print('Encontrado')