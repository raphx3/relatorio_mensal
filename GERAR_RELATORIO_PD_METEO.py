#%% Modulos
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import datetime as dtt
import streamlit as st
import time
#from QC_FLAGS_UMISAN_VER08_REVRA import *
#from QC_OPERACIONAL_UMISAN_VER09_REVRA import * # é de onde vem a variavel df 
from QC_FLAGS_UMISAN import *
from OPERACIONAL_UMI_SIMPLIFICADO import *

#%% FRONT END STREAMLIT


import os
import streamlit as st
import pandas as pd
import time

import os
import streamlit as st
import pandas as pd
import time

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

    col1, col2 = st.columns(2)
    with col1:
        data_inicio = st.date_input('Data de início:', pd.to_datetime('2024-01-01'))
    
    with col2:
        data_fim = st.date_input('Data de fim:', pd.to_datetime('2025-12-31'))

    pasta_saida = st.text_input(
        'Insira o caminho da pasta onde os resultados serão salvos:', 
        r'C:\Users\Rafael Alvarenga UMI\Desktop\PD_METEO\REPORTES\RELATORIO_MENSAL\RESULTADOS',
        key='input_pasta_saida'
    )

    # Gerando os resultados para o download
    if st.button(label='Gerar Resultados para Relatório'):
        try:
            # Simulando a criação de um arquivo, por exemplo um CSV ou PDF
            df = pd.DataFrame({
                'Data': pd.date_range(start=data_inicio, end=data_fim, freq='D'),
                'Valor': range((data_fim - data_inicio).days + 1)
            })

            # Crie o conteúdo do arquivo (aqui um CSV, mas pode ser outro formato)
            file_content = df.to_csv(index=False)
            
            # Gerar o download do arquivo diretamente com st.download_button
            st.download_button(
                label="Download do Relatório",
                data=file_content,
                file_name="relatorio_mensal.csv",
                mime="text/csv"
            )
            
            st.success("Relatório gerado com sucesso para download!")

        except Exception as e:
            st.error(f"Erro ao gerar os resultados: {e}")





#%% filtrar_por_periodo

def filtrar_por_periodo(df, data_inicio, data_fim):
    
    # Filtro
    data_inicio = pd.to_datetime(data_inicio)
    data_fim = pd.to_datetime(data_fim)
    df_filtrado_por_tempo = df[(df['GMT-03:00'] >= data_inicio) & (df['GMT-03:00'] <= data_fim)]
    
    return df_filtrado_por_tempo, data_inicio.strftime("%Y-%m-%d %H:%M:%S"), data_fim.strftime("%Y-%m-%d %H:%M:%S")



#%% Dicionários
# Parametros de interesse dados maré
parameter_columns_mare = [
    'GMT-03:00', 
    'Pressure_S1',
    'Pressure_S2', 

    ]
# Parametros de interesse dados meteorologicos
parameter_columns_meteo= [
    'GMT-03:00',
    'Pressure(hPa)', 
    'Rain', 
    'Wind Direction(*)',
    'Gust Speed(m/s)',
    'Wind Speed(m/s)', 
    'Dew Point',
    'RH(%)',
    'Temperature(*C)'
    ]

# Parametros de interesse dados correntes
parameter_columns_correntes=[
    'GMT-03:00',
    'Battery',
    'Heading',
    'Pitch',
    'Roll',
    'Pressure(dbar)',
    'Temperature(C)',
    ]

# Parametros de interesse dados ondas
parameter_columns_ondas = [
    'GMT-03:00',  # Data e hora no fuso horário GMT-03:00 (horário de Brasília ou outro fuso horário local),
    'Hm0',  # Altura significativa das ondas (m), média das maiores 1/3 das ondas em um período de tempo
    'Hmax',  # Altura máxima das ondas (m), a maior altura registrada das ondas em um período de tempo
    'Hm0_sea',  # Altura significativa das ondas no mar (m)
    'Hm0_swell',  # Altura significativa das ondas na ondulação (m),
    'Tm02',  # Período médio de onda (s), tempo médio entre duas ondas consecutivas
    'Tp',  # Período de pico das ondas (s), o período associado à maior energia no espectro de ondas
    'Tp_sea',  # Período de pico das ondas no mar (s)
    'Tp_swell',  # Período de pico das ondas na ondulação (s),
    'DirTp',  # Direção do período de pico das ondas (graus), direção de propagação das ondas associadas ao Tp
    'DirTp_sea',  # Direção do período de pico das ondas no mar (graus)
    'DirTp_swell',  # Direção do período de pico das ondas na ondulação (graus)
    'Main Direction',  # Direção principal das ondas (graus), direção predominante das ondas
    'Main Direction_sea',  # Direção principal das ondas no mar (graus)
    'Main Direction_swell',  # Direção principal das ondas na ondulação (graus)
    'Mean pressure',  # Pressão média (não especificada)
    'Battery',  # Nível da bateria do sensor
    'Heading',  # Rumo ou direção da embarcação/sensor (graus)
    'Pitch',  # Inclinação do sensor em relação ao eixo horizontal (graus)
    'Roll',  # Inclinação lateral do sensor (graus)
    'Pressure(dbar)',  # Pressão medida (dbar)
    'Temperature(C)',  # Temperatura da água (°C)
]

parameter_columns_ondas_nao_direcionais = [
    'GMT-03:00',
    'Tide_Level',
    "Sensor_Velki", 
    'CutOff_Freq_High',
    'Peak_Period',
    'Mean_Period',
    'Max_Height',
    'Sign_Height',

    
    ]

func_names = [
    "time_offset", 
    "range_check_sensors", 
    "range_check_environment", 
    "identificar_gaps", 
    "identificar_dados_nulos", 
    "spike_test", 
    "lt_time_series_rate_of_change", 
    "teste_continuidade_tempo", 
    "identificar_duplicatas_tempo", 
    "verifica_dados_repetidos", 
    "st_time_series_segment_shift", 
    "max_min_test", 
    "verificar_temperatura_vs_ponto_de_orvalho", 
    "verificar_velocidade_vs_rajada", 
    "verificar_altura_max_vs_sig", 
    "gradiente_de_amplitude_do_sinal", 
    "detectar_platos", 
    "taxa_de_mudanca_vertical"
]





#%% plot_series_temporais
import io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dtt
import streamlit as st

def plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste):  
    agora = dtt.datetime.now()
    agora = agora.strftime('%Y/%m/%d %H:%M:%S')
    
    # Encontrar as colunas de "Amplitude" e "Speed"
    amplitude_cols = [col for col in df_filtrado.columns if "Amplitude" in col and "Flag_" not in col and "GMT-03:00" not in col]
    speed_cols = [col for col in df_filtrado.columns if "Speed" in col and "Flag_" not in col and "GMT-03:00" not in col]

    # Garantir que as colunas de "Amplitude" sejam numéricas
    df_amplitude = df_filtrado[amplitude_cols].apply(pd.to_numeric, errors='coerce')
    df_speed = df_filtrado[speed_cols].apply(pd.to_numeric, errors='coerce')

    if not df_amplitude.empty:
        ymin_amplitude = df_amplitude.min().min() * 0.7
        ymax_amplitude = df_amplitude.max().max() * 1.3

    if not df_speed.empty:
        ymin_speed = df_speed.max().max() * -0.1
        ymax_speed = df_speed.max().max() * 1.1

    images_for_download = []  # Lista para armazenar imagens em memória

    for param in parameter_columns:
        flag_column = f'Flag_{param}'

        if flag_column in df_filtrado.columns:
            plt.figure(figsize=(12, 6))
            plt.gca().set_facecolor('white')

            # Separar os dados por flag
            df_preenchido = df_filtrado.copy()
            df_preenchido = df_preenchido.fillna(df_preenchido.mean())
            df_flag_0 = df_preenchido[df_preenchido[flag_column] != 4]
            df_flag_4 = df_preenchido[df_preenchido[flag_column] == 4]

            # Contagem de dados por flags
            count_flag_0 = len(df_flag_0)
            count_flag_4 = len(df_flag_4)
            porcentagem_flag_0 = round((count_flag_0 / len(df_filtrado)) * 100, 2)
            porcentagem_flag_4 = round((count_flag_4 / len(df_filtrado)) * 100, 2)

            # Plotar série completa
            plt.plot(df_filtrado['GMT-03:00'], df_filtrado[param], label=f'Série Completa: Flag 0 ({porcentagem_flag_0}%)', alpha=0.7, color='black', linestyle='-', linewidth=1, zorder=1)

            # Plotar os dados com Flag 4 (vermelho) como pontos
            plt.scatter(df_flag_4['GMT-03:00'], df_flag_4[param], color='red', alpha=1, s=15, label=f'Flag 4 ({porcentagem_flag_4}%)', zorder=2)

            # Configurações do gráfico
            data_inicio = str(df_filtrado['GMT-03:00'].iloc[0])
            data_fim = str(df_filtrado['GMT-03:00'].iloc[-1])
            plt.title(f'Série Temporal: {parametro_para_teste} - {param} - execução do reporte: {agora}\nPeríodo de análise: {data_inicio} - {data_fim}')
            plt.xlabel('Tempo (Data/Hora)')

            if "Amplitude" in param:
                plt.ylabel('Amplitude (m)')
            if "Speed" in param:
                plt.ylabel('Velocidade (m/s)')
            if "Direction" in param:
                plt.ylabel('Direção (°)')
            
            # Garantir 5 ticks no eixo X
            time_min = df_filtrado['GMT-03:00'].min()
            time_max = df_filtrado['GMT-03:00'].max()
            xticks_positions_timestamp = np.linspace(time_min.timestamp(), time_max.timestamp(), 5)
            xticks_positions = [pd.to_datetime(ts, unit='s') for ts in xticks_positions_timestamp]
            plt.xticks(xticks_positions, rotation=0)

            if param in amplitude_cols:
                plt.ylim(ymin_amplitude, ymax_amplitude)
            if param in speed_cols:
                plt.ylim(ymin_speed, ymax_speed)

            plt.legend(loc='upper right')
            plt.grid(True, linestyle='dotted', alpha=0.5)

            # Salvar a figura em memória
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)  # Voltar para o começo do arquivo para leitura

            # Adicionar a imagem à lista de imagens para download
            images_for_download.append((f'{parametro_para_teste} - {param} - {data_inicio} a {data_fim}.png', img_bytes))

            plt.close()

    # Adicionar os botões de download para cada imagem gerada
    for file_name, img_bytes in images_for_download:
        st.download_button(
            label=f"Baixar {file_name}",
            data=img_bytes,
            file_name=file_name,
            mime="image/png"
        )

    st.success("Relatório gerado com sucesso!")

# Função de execução no Streamlit
def exibir_pagina_streamlit():
    st.title('Relatório de Séries Temporais')

    # Suponha que df_filtrado e parameter_columns já estejam definidos aqui
    # df_filtrado: DataFrame com dados temporais
    # parameter_columns: lista de colunas de parâmetros a serem processadas

    # Exemplo de chamada da função com dados simulados (substitua com seus dados reais)
    df_filtrado = pd.DataFrame({
        'GMT-03:00': pd.date_range(start='2024-01-01', periods=100, freq='H'),
        'Amplitude1': np.random.rand(100),
        'Speed1': np.random.rand(100),
        'Flag_Amplitude1': np.random.choice([0, 4], size=100),
    })
    parameter_columns = ['Amplitude1', 'Speed1']

    plot_series_temporais(df_filtrado, parameter_columns, "Exemplo de Parâmetro")



#%% Executando a função para exibir a página no Streamlit


def main():
    
   
    # Chamando a função do Streamlit para exibir a página
    exibir_pagina_streamlit()

# Chama a função principal se o arquivo for executado diretamente
if __name__ == "__main__":
    main()

