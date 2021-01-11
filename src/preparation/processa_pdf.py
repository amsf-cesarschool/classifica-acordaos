# -*- coding: utf-8 -*-
"""
Created on Sun Aug 23 12:41:15 2020

@author: antonio.moreira
"""
import sys
sys.path.append('../')
import acordaos_utils

import pdfplumber

def extrai_acordao(caminho):
    try:
        path = acordaos_utils.caminho_completo(caminho)
    except FileExistsError as erro:
        raise erro

    texto_acordao = ''
    linhas_acordao = []
    cabecalho = []
    acordao_encontrado = False

    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            lines = extrac_lines(page)
            
            print(len(lines))
            if page.page_number == 1:
                if len(lines) == 0:
                    return None, None

                testar_se_cabecalho = False
            else:
                testar_se_cabecalho = True
                
            for line in lines:
                texto_linha = acordaos_utils.clean_text(line['text'])
                if testar_se_cabecalho:
                    if texto_linha in cabecalho: 
                        continue
                    else: testar_se_cabecalho = False
                
                if (not acordao_encontrado):
                    if (texto_linha.startswith('acordao') or
                        texto_linha.startswith('parecer previo')):
                        texto_acordao = texto_acordao + line['text'].strip() + '\n'
                        linhas_acordao.append(line)
                        acordao_encontrado = True
                    else:
                        cabecalho.append(texto_linha)
                    
                    continue
                
                texto_acordao = texto_acordao + line['text'].strip() + '\n'
                linhas_acordao.append(line)
    return texto_acordao, linhas_acordao

def extrac_lines(page):
    words = page.extract_words(keep_blank_chars=True)
    lines = []
   
    line_text = ''
    bottom_line = 0
    initial_x0 = 0
    final_x1 = 0
    
    try:
        for word in words:
            actual_bottom = int(word['bottom'])
            if (actual_bottom - bottom_line) > 5:  # Nova linha
                if (bottom_line != 0): # se não for primeira linha, adiciona
                    lines.append({'page': page.page_number, \
                                  'x0': initial_x0, 'x1': final_x1, \
                                      'bottom': bottom_line, \
                                'text': line_text})

                line_text = ''
                bottom_line = actual_bottom
                initial_x0 = int(word['x0'])

            line_text = line_text + word['text']
            final_x1 = int(word['x1'])
            #x0, x1, top, bottom, text = word
    except:
        return []
    return lines

#%% 
#texto, linhas = extrai_acordao('/2019/02/749088/119/75/856temp/ACO.pdf')
#texto, linhas = extrai_acordao('/2013/11/533724/120/42/644temp/PARPRE_assinado_assinado_assinado.pdf')
#print(texto)
