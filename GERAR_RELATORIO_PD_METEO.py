# %% Módulos
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dtt
import streamlit as st
import time
import io
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from QC_FLAGS_UMISAN import *
from OPERACIONAL_UMI_SIMPLIFICADO import *

# %% FUNÇÕES DE GERAÇÃO DE GRÁFICOS

def plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste):
    agora = dtt.datetime.now()
    agora = agora.strftime('%Y/%m/%d %H:%M:%S')

    # Encontrar as colunas que possuem "Amplitude" no nome (excluindo "Flag_")
    amplitude_cols = [col for col in df_filtrado.columns if "Amplitude" in col and "Flag_" not in col  and "GMT-03:00" not in col]
    speed_cols = [col for col in df_filtrado.columns if "Speed" in col and "Flag_" not in col  and "GMT-03:00" not in col]
    
    # Garantir que as colunas de "Amplitude" sejam numéricas, descartando valores não numéricos
    df_amplitude = df_filtrado[amplitude_cols].apply(pd.to_numeric, errors='coerce')
    df_speed = df_filtrado[speed_cols].apply(pd.to_numeric, errors='coerce')
    
    # Calcular os limites globais do eixo Y com base nas colunas "Amplitude"
    if not df_amplitude.empty:
        ymin_amplitude = df_amplitude.min().min()*0.7
        ymax_amplitude = df_amplitude.max().max()*1.3
    
    if not df_speed.empty:
        ymin_speed = df_speed.max().max()*-0.1
        ymax_speed = df_speed.max().max()*1.1
    
    # Criar gráfico em memória
    fig, ax = plt.subplots(figsize=(12, 6))
    
    for param in parameter_columns:
        flag_column = f'Flag_{param}'
        
        if flag_column in df_filtrado.columns:
            df_preenchido = df_filtrado.fillna(df_filtrado.mean())
            df_flag_0 = df_preenchido[df_preenchido[flag_column] != 4]
            df_flag_4 = df_preenchido[df_preenchido[flag_column] == 4]
            df_nan = df_filtrado[df_filtrado[param].isna()].fillna(df_filtrado.mean())
            
            # Plotar série completa
            ax.plot(df_filtrado['GMT-03:00'], df_filtrado[param], label=f'Série Completa', alpha=0.7, color='black', linestyle='-', linewidth=1)
            
            # Plotar dados com Flag 4 (vermelho) como pontos
            ax.scatter(df_flag_4['GMT-03:00'], df_flag_4[param], color='red', alpha=1, s=15, label=f'Flag 4')
            
            # Plotar os nan como a média da série temporal
            ax.plot(df_nan['GMT-03:00'], df_nan[param], alpha=0.8, color='black', linestyle='dotted', linewidth=1, label='Valores nulos')

            ax.set_title(f'Série Temporal: {parametro_para_teste} - {param} - execução do reporte: {agora}')
            ax.set_xlabel('Tempo (Data/Hora)')
            
            # Ajustar o eixo Y conforme o tipo de dado
            if param in amplitude_cols:
                ax.set_ylabel('Amplitude (m)')
                ax.set_ylim(ymin_amplitude, ymax_amplitude)
            if param in speed_cols:
                ax.set_ylabel('Velocidade (m/s)')
                ax.set_ylim(ymin_speed, ymax_speed)
            # Outros casos de parâmetros podem ser adicionados aqui

            ax.grid(True, linestyle='dotted', alpha=0.5)
            ax.legend(loc='upper right')

    # Gerar o gráfico em um buffer de memória
    buf = io.BytesIO()
    FigureCanvas(fig).print_png(buf)
    buf.seek(0)  # Voltar ao início do arquivo para o download

    return buf

# %% FUNÇÃO PRINCIPAL STREAMLIT

def exibir_pagina_streamlit():
    st.title('Relatório mensal')
    
    # Campos para o usuário inserir informações de configuração de teste
    analista = st.text_input('Nome do Analista:', 'Raphael')  # Nome do analista
    projeto = st.text_input('Nome do Projeto:', 'PD_METEO')  # Nome do projeto
    boia = st.text_input('Nome da Boia:', 'Protótipo 1')  # Nome da boia
    
    # Seleção do parâmetro para teste
    parametro_para_teste = st.selectbox(
        'Selecione o parâmetro para teste:',
        ['CORRENTES', 'METEOROLOGIA', 'MARE', 'ONDAS', 'ONDAS_NAO_DIRECIONAIS']
    )

    # Usando st.columns() para criar colunas lado a lado
    col1, col2 = st.columns(2)  # Cria duas colunas

    # Campo para o usuário inserir as datas de início e fim lado a lado
    with col1:
        data_inicio = st.date_input('Data de início:', pd.to_datetime('2024-01-01'))
    
    with col2:
        data_fim = st.date_input('Data de fim:', pd.to_datetime('2025-12-31'))

    # Campos de seleção de parâmetros
    if parametro_para_teste == 'CORRENTES':
        parameter_columns = parameter_columns_correntes
    elif parametro_para_teste == 'METEOROLOGIA':
        parameter_columns = parameter_columns_meteo
    elif parametro_para_teste == 'MARE':
        parameter_columns = parameter_columns_mare
    elif parametro_para_teste == 'ONDAS':
        parameter_columns = parameter_columns_ondas
    elif parametro_para_teste == 'ONDAS_NAO_DIRECIONAIS':
        parameter_columns = parameter_columns_ondas_nao_direcionais
    
    # Botão para gerar os resultados e salvar na pasta
    if st.button(label='Gerar Resultados para Relatório na Pasta Selecionada'):
        try:
            # Exemplo de dados (substitua com os seus dados reais)
            df_filtrado_por_tempo = pd.DataFrame({
                'GMT-03:00': pd.date_range(start='2023-01-01', periods=100, freq='D'),
                'Amplitude_S1': np.random.rand(100) * 10,
                'Speed_S1': np.random.rand(100) * 20,
                'Flag_Amplitude_S1': np.random.choice([0, 4], size=100),
                'Flag_Speed_S1': np.random.choice([0, 4], size=100),
            })
            
            # Filtrando dados por período
            df_filtrado_por_tempo, inicio, fim = filtrar_por_periodo(df_filtrado_por_tempo, data_inicio, data_fim)
            
            # Gerar o gráfico na memória
            buf = plot_series_temporais(df_filtrado_por_tempo, parameter_columns, parametro_para_teste)
            
            # Exibir o botão de download
            st.download_button(
                label="Baixar Gráfico",
                data=buf,
                file_name="grafico_serie_temporal.png",
                mime="image/png"
            )
            st.success("Relatório gerado com sucesso!")
        
        except Exception as e:
            st.error(f"Erro ao gerar os resultados: {e}")

# %% FILTRO DE PERÍODO

def filtrar_por_periodo(df, data_inicio, data_fim):
    # Filtro
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    df_filtrado_por_tempo = df[(df['GMT-03:00'] >= data_inicio) & (df['GMT-03:00'] <= data_fim)]
    
    return df_filtrado_por_tempo, data_inicio.strftime("%Y-%m-%d %H:%M:%S"), data_fim.strftime("%Y-%m-%d %H:%M:%S")

# %% EXECUÇÃO DO STREAMLIT

if __name__ == "__main__":
    exibir_pagina_streamlit()
