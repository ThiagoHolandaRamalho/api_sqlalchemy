import random
import time
import random
from controller import importar_registros_cyber , buscar_bilhetes
from multiprocessing import Pool, cpu_count
from tqdm import tqdm

from joblib import Parallel, delayed
import sys

bilhete_inicial = 178764750 +2000
bilhetes = []

for i in range(0,10):
    bilhetes.append(bilhete_inicial+i)

#lista_execucao_paralela = Parallel(n_jobs= 5)(delayed(importar_registros_cyber)(bilhete) for bilhete in bilhetes)





def processar_bilhetes():
    with Pool(10) as pool:
        for i in tqdm(pool.imap_unordered(importar_registros_cyber,bilhetes), total=len(bilhetes),position=0, leave=True):
            ...
        #resultados = pool.imap_unordered(importar_registros_cyber, bilhetes)
        #for resultado in resultados:
        #    pass
 
if __name__ == "__main__":
    res = processar_bilhetes()
