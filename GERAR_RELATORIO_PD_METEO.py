import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dtt
import streamlit as st
import time
import tempfile

# Função para criar gráfico e retornar como arquivo
def gerar_grafico(df, parametro_para_teste, output_path):
    # Exemplo de gráfico (você pode customizar o tipo de gráfico conforme necessário)
    plt.figure(figsize=(10, 6))
    plt.plot(df['DATA'], df['VALOR'])  # Ajuste conforme as colunas do seu DataFrame
    plt.title(f'Gráfico de {parametro_para_teste}')
    plt.xlabel('Data')
    plt.ylabel('Valor')
    
    # Salvar o gráfico como uma imagem temporária
    plt.savefig(output_path)
    plt.close()

# Função principal para exibir a página no Streamlit
def exibir_pagina_streamlit():
    st.title('Relatório mensal')
    
    # Campos para o usuário inserir informações de configuração de teste
    analista = st.text_input('Nome do Analista:', 'Raphael')  
    projeto = st.text_input('Nome do Projeto:', 'PD_METEO')  
    boia = st.text_input('Nome da Boia:', 'Protótipo 1')  
    
    parametro_para_teste = st.selectbox(
        'Selecione o parâmetro para teste:',
        ['CORRENTES', 'METEOROLOGIA', 'MARE', 'ONDAS', 'ONDAS_NAO_DIRECIONAIS']
    )

    # Usando st.columns() para criar colunas lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        data_inicio = st.date_input('Data de início:', pd.to_datetime('2024-01-01'))
    
    with col2:
        data_fim = st.date_input('Data de fim:', pd.to_datetime('2025-12-31'))

    # Campo para o usuário inserir o caminho da pasta onde os resultados serão salvos
    pasta_saida = st.text_input(
        'Insira o caminho da pasta onde os resultados serão salvos:', 
        r'C:\Users\Rafael Alvarenga UMI\Desktop\PD_METEO\REPORTES\RELATORIO_MENSAL\RESULTADOS',
        key='input_pasta_saida'
    )

    # Botão para gerar os resultados e salvar na pasta
    if st.button(label='Gerar Resultados para Relatório na Pasta Selecionada'):
        if pasta_saida:
            # Cria uma pasta temporária para salvar as imagens (para evitar problemas de caminho)
            with tempfile.TemporaryDirectory() as tmpdirname:
                # Gerar o gráfico
                try:
                    # Supondo que 'df' é o DataFrame que contém os dados filtrados
                    df = pd.DataFrame({'DATA': pd.date_range(start='2024-01-01', periods=10, freq='D'),
                                       'VALOR': np.random.rand(10)})
                    output_path = os.path.join(tmpdirname, f'{parametro_para_teste}_grafico.png')
                    
                    # Gerando o gráfico
                    gerar_grafico(df, parametro_para_teste, output_path)
                    
                    # Exibindo botão de download
                    with open(output_path, "rb") as f:
                        st.download_button(
                            label="Baixar Gráfico",
                            data=f,
                            file_name=f'{parametro_para_teste}_grafico.png',
                            mime="image/png"
                        )
                    
                    st.success(f"Gráfico gerado com sucesso!")
                
                except Exception as e:
                    st.error(f"Erro ao gerar o gráfico: {e}")

