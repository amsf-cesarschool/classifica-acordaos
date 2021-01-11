# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 11:13:55 2020

@author: antonio.moreira
"""
import unicodedata
from pathlib import Path

def caminho_incial(ano_mes):
    ano, mes = ano_mes.split('/')

    if int(ano) >= 2020:
        return "//alya/ftpd$/etce/"
    elif (int(ano) == 2013 and int(mes) == 11):
        return "//alya/ftpf$/etce/"
    else:
        caminhos = {"2012": "//alya/ftpd$/etce/", \
                    "2013": "//alya/ftpd$/etce/", \
                    "2014": "//alya/ftpf$/etce/", \
                    "2015": "//alya/ftpf$/etce/", \
                    "2016": "//alya/ftpd$/etce/", \
                    "2017": "//alya/ftpd$/etce/", \
                    "2018": "//alya/ftpd$/etce/", \
                    "2019": "//alya/ftpg$/etce/"}
        return caminhos[ano]

def caminho_completo(caminho):
    path = Path(caminho_incial((caminho)[1:8]) + caminho)
    if path.exists():
        return path
    else:
        raise FileExistsError(f"Arquivo não encontrado para {caminho}")

def clean_text(text):
    return unicodedata.normalize("NFD", text).encode('ASCII','ignore').decode('ASCII').replace("  ", " ").casefold().strip()

#%% testes
#print(caminho_completo('/2013/11/533724/120/42/644temp/PARPRE_assinado_assinado_assinado.pdf'))
#print(extrai_cod_tce('TC/52917/2012'))