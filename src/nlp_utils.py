# -*- coding: utf-8 -*-
"""
Created on Wed Oct  7 17:14:08 2020

@author: antonio.moreira
Aadaptado de https://github.com/netoferraz/o-eu-analitico/blob/master/_notebooks/2020-07-26-gov-data-product-p3.ipynb
"""

#Imports
import re
import unicodedata

from nltk import word_tokenize

# Excluir tokens que sejam compostos exclusivamente de dígitos.
def hasNumbers(inputString):
    return any(char.isdigit() for char in inputString)

#Normalizar os tokens de forma a retirar acentos e caracteres especiais.
def removerAcentosECaracteresEspeciais(palavra):
    # Unicode normalize transforma um caracter em seu equivalente em latin.
    nfkd = unicodedata.normalize('NFKD', palavra)
    palavraSemAcento = u"".join([c for c in nfkd if not unicodedata.combining(c)])
    #retirar espaços vazios múltiplos
    palavraSemAcento = re.sub(' +', ' ', palavraSemAcento)
    # Usa expressão regular para retornar a palavra apenas com números, letras e espaço
    return re.sub('[^a-zA-Z0-9 \\\]', '', palavraSemAcento).lower()

#Correção de grafia de tokens
#Xcorreção da ocorrência de alguns tokens que estão com grafia incorreta, 
#ou duas palavras que não estão separadas por espaço, ou mesmo palavras no plural que vamos transformá-la para o singular.
def split_selected_tokens(texto: str):
    select_tokens = {
        'dedezembro' : 'de dezembro',
        'capitalsocial' : 'capital social',
        'decretosleis' : 'decretos leis',
        'nacionaldestinada' : 'nacional destinada',
        'professorequivalente' : 'professor equivalente',
        'tvsbt' : 'tv sbt',
        'orcamentariavigente' : 'orcamentaria vigente',
        'tecnicoprofissional' : 'tecnico profissional',
        'republicafederativa' : 'republica federativa', 
        'transbrasilianaconcessionaria' : 'transbrasiliana concessionaria',
        'publicoprivada' : 'publico privada',
        'procuradorgeral' : 'procurador geral',
        'auditoriafiscal' : 'auditoria fiscal',
        'decretoslei' : 'decretos lei',
        'segurancapublica' : 'seguranca publica',
        'novadutra' : 'nova dutra',
        'queespecifica' : 'que especifica',
        'agenciasreguladoras' : 'agencias reguladoras',
        'autopistalitoral' : 'autopista litoral',
        'goiasvigencia' : 'goias vigencia',
        'governadorcelso' : 'governador celso',
        'autopistaregis' :'autopista regis',
        'valecultura' : 'vale cultura',
        'programacaoorcamentaria' : 'programacao orcamentaria',
        'dopoder' : 'do poder',
        'ministeriodo' : 'ministerio do',
        'estadosmembros' : 'estados membros',
        'papelmoeda' :'papel moeda',
        'bolsaatleta' : 'bolsa atleta',
        'complementacaoeconomica' : 'complementacao economica',
        'artisticoculturais' :'artistico culturais',
        'conselhogeral' : 'conselho geral',
        'tecnicoadministrativos' : 'tecnico administrativos',
        'registradosacrescentando' : 'registrado sacrescentando',
        'ruralcontratadas' : 'rural contratadas',
        'estudantesconvenio' : 'estudantes convenio',
        'delegadode' : 'delegado de',
        'junhode' : 'junho de',
        'denovembro' : 'de novembro',
        'lavourapecuariafloresta' : 'lavoura pecuaria floresta',
        'autorizadaaltera' : 'autorizada altera',
        'grupodefesa' : 'grupo defesa',
        'contribuicoesprevidenciarias' : 'contribuicoes previdenciarias',
        'cpfgce' : 'cpf gce',
        'empregose' : 'empregos e',
        'dosanistiados' : 'dos anistiados',
        'antigomobilismo' : 'antigo mobilismo',
        'dogrupodirecao' : 'do grupo direcao',
        'milhoestrezentos' : 'milhoes trezentos',
        'deavaliacao' : 'de avaliacao',
        'salariominimo' : 'salario minimo',
        'imoveis' : 'imovel',
        'grupodirecao' : 'grupo direcao',
        'pispasep' : 'pis pasep',
        'rurais' : 'rural'
    }
    new_text = texto.split(" ")
    container =[]
    for word in new_text:
        if word in select_tokens.keys():
            container.append(select_tokens[word])
        else:
            container.append(word)
    return " ".join(container)

# Consolidação uma função que agrega as nossas etapas de pré-processamento.
def pre_processing_pipeline(texto:str):
    texto = " ".join([token for token in word_tokenize(removerAcentosECaracteresEspeciais(texto)) if not token.isdigit()])

    texto = " ".join([token for token in word_tokenize(texto) if not hasNumbers(token)])

    texto = " ".join([token for token in word_tokenize(texto) if len(token) > 2])
    texto = " ".join([split_selected_tokens(token) for token in word_tokenize(texto) if not token.isdigit()])
    return texto