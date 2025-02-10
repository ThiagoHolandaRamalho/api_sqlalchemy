import random
import time
import random
from controller import buscar_bilhetes, importar_bilhete,filtrar_bilhete,buscar_parcelas_cyber,importar_parcelas_bilhetes_cyber,filtrar_parcelas_bilhete
from multiprocessing import Pool, cpu_count


bilhete_inicial = 171164750

for i in range(0,3):
    new_bilhete = bilhete_inicial+i
    
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
            #print(f'Sucesso parcelas {new_bilhete}')
    
    else:
        print(f'parcelas vazias {new_bilhete}')
