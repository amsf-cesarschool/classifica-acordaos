# -*- coding: utf-8 -*-
"""
Created on Tue Sep 15 22:09:34 2020
@author: antonio.moreira

Importa os boletins de jurisprudência.
São estraídos os seguintes campo do boletim no formato word:
Sumário     Resumo do acórdão digitado pelo Analista durante confecção do Boletim.
            É iniciado pela área temática seguida de um ponto. 
            Não corresponde ao conteúdo do sumário do acórdão.
Ementa      Ementa presente no acórdão.
Informações Resumo das informações processuais presentes no acórdão.
            Digitada pelo Analista.
            Contém campos número do processo e publicacao_DOU que estão como links e, 
            por isso, não foi possível extrair.

Campo AreaTematica é extraído do Sumário
Campos do acórdão (tipo_decisão, número e ano) são extraídos a partir de 'Informações'
###############################
Antonio Filho - 13/11/2020 (Após uso de dados naa análises para dissertação)
Importar boletim de 10/2020 e salvar em arquivo á parte 
"""
#%% Importação das bibliotecas
import docx
import pandas as pd
import re

from pathlib import Path
import os

import sys
sys.path.append('../')
import processa_acordao
#%% Fazer leirura dos boletins
# Retornar ano-mes a partir do nome do arquivo no formato AAAA-MM
def anomes(arquivo):
    meses = {'janeiro': '01', 'fevereiro': '02', 'março': '03', 'abril': '04', 'maio': '05', 'junho': '06', \
             'julho': '07', 'agosto': '08', 'setembro': '09', 'outubro': '10', 'novembro': '11', 'dezembro': '12'}
    pattern = r"\w+\s?[-]?\s?\d+"

    match = re.search(pattern, arquivo)
    anomes = match.group(0)
    mes = re.search(r"\w+", anomes).group().strip().lower()
    ano = re.search(r"\d+", anomes).group().strip()
    ano = pd.to_datetime(ano, format='%y' if len(ano)==2 else '%Y').year
    return str(ano) + '-' + meses.get(mes)

CAMINHO = Path('../../data/raw/boletins-jurisprudencia')
files = [f for r, d, f in os.walk(CAMINHO)]
boletins = []
for filename in files[0]:
    pattern = "^Boletim(.)*.docx$"
    if re.search(pattern, filename):
        print('Importando: ', filename)
        doc = docx.Document(CAMINHO/filename)
        is_in_Ementa = False
        for paragraph in doc.paragraphs:
            if len(paragraph.text.strip()) == 0:
                continue
            
            #if paragraph.style.name == 'Heading 2':
            if (not paragraph.paragraph_format.left_indent and not is_in_Ementa and len(paragraph.text) > 34):
                boletim = dict()
                boletim['arquivo'] = filename
                boletim['ano_mes'] = anomes(filename)
                boletim['sumario'] = paragraph.text.strip()
                is_in_Ementa = True
            else:
                if paragraph.text.strip().startswith('('):
                    boletim['informacoes'] = paragraph.text.strip()
                    boletins.append(boletim)
                    is_in_Ementa = False
                elif is_in_Ementa:
                    if boletim.get('ementa') != None:
                        ementa = boletim.get('ementa') + '\n' 
                    else:
                        ementa = '' 
                
                    boletim['ementa'] = ementa + paragraph.text.lstrip()

#%% Gerar dataframe de boletins
df = pd.DataFrame(boletins)

#%% Criar coluna AreaTematica
df['area_tematica'] = df['sumario'].apply(lambda x: x.split('.')[0])

#%% Extrair dados do Acórdão
for ind in df.index:
    tipo, numero, ano = processa_acordao.extrai_tipo_numero_ano(df.loc[ind, 'informacoes'])
    df.loc[ind, ['decisao_tipo', 'decisao_numero', 'decisao_ano']] = tipo, numero, ano

#%%
print('Salvando dataframe em csv')
CAMINHO = Path('../../data/raw/')
df.to_csv(CAMINHO/"boletins_jurisprudencia2.csv", sep=';', index=False)