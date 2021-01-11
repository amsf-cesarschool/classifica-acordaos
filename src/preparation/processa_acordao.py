# -*- coding: utf-8 -*-
"""
Created on Tue Aug 25 05:32:32 2020

@author: antonio.moreira
"""
import sys
sys.path.append('../')
from  acordaos_utils import clean_text

import re

def extrai_tipo_numero_ano(texto):
    if isinstance(texto, str):
        texto_pesquisar = clean_text(texto)
        pattern = r"acordao.{1,10}[\d.]+[\s|-]*[a-z]?\s?/?/[\d.]+"
        match = re.search(pattern, texto_pesquisar, re.IGNORECASE)
        if match: tipo = 'acordao'
        else:
            pattern = r"parecer\s{1,2}previo.{1,10}[\d.]+[\s|-]*[a-z]?\s?/?/[\d.]+"
            match = re.search(pattern, texto_pesquisar, re.IGNORECASE)
            if match: tipo = 'parecer'
            else:
                return None, None, None
        
        codigo = match.group(0).replace("//", "/")
        numero, ano = extrai_numero_ano(codigo)
        return tipo, numero, int(ano)
        
    return None, None, None

def extrai_numero_ano(codigo):
    if isinstance(codigo, str):
        pattern = r"[\d.]+[\s|-]*[a-z]?\s?/[\d.]+"
        match = re.search(pattern, codigo, re.IGNORECASE)
        if match:
            numero, ano = match.group(0).split('/')
            numero = numero.replace('.', '').replace(" ", "").upper()
            if numero.isnumeric():
                numero = str(int(numero))   #Remover zeros a esquerda
            ano = ano.replace('.', '')
            if len(ano) == 2:
                ano = '20' + ano
            return numero, int(ano)
        
    return None, None

def extrai_cod_tce(processo):
    pattern = r"[\d.]+/\d+"  # Apenas digitos ou ponto seguido por / e digitos
    
    #print(processo)
    match = re.search(pattern, processo)
    if match:
        cod_tce = re.search(pattern, processo).group(0)
        numero, ano = cod_tce.split('/')
        numero = numero.replace('.', '')
        if len(ano) == 2:
            ano = '20' + ano
        cod_tce = str(numero).zfill(6) + '/' + ano
        return cod_tce

def processo_ajustado(processo):
    pattern = r"[\d.]+/\d+"  # Apenas digitos ou ponto seguido por / e digitos
    
    #print(processo)
    match = re.search(pattern, processo)
    if match:
        cod_tce = re.search(pattern, processo).group(0)
        numero, ano = cod_tce.split('/')
        numero = numero.replace('.', '')
        if len(ano) == 2:
            ano = '20' + ano
        cod_tce = str(numero).zfill(6) + '/' + ano
        return 'TC/' + cod_tce
    else:
        return processo
    
def cod_tce_eh_valido(cod_tce):
    numero, _ = cod_tce.split('/')
    return len(numero) == 6

def teste():
    tipo, numero, ano = extrai_tipo_numero_ano('ACÓRDÃO Nº 1.854-A/2019 (R.R)	\nPROCESSO')
    #tipo, numero, ano = extrai_tipo_numero_ano('1.854-A/2019 (R.R)	')
    print(tipo, ':', numero, '/', ano)

#%%
#teste()

#tipo, numero, ano  = extrai_tipo_numero_ano('PARECER PRÉVIO Nº 65/2019\n')
#print(tipo, numero, ano)
#print(extrai_cod_tce('TC/52917/2012'))
