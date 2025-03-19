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
import io

#%% FRONT END STREAMLIT


def exibir_pagina_streamlit():
    st.title("Análise de Séries Temporais")
    
    # Passo 1: Upload dos dados
    uploaded_file = st.file_uploader("Carregar arquivo CSV", type="csv")
    
    if uploaded_file is not None:
        # Passo 2: Carregar os dados em um DataFrame
        df_filtrado = pd.read_csv(uploaded_file)
        st.write("Visualizando os primeiros dados carregados:", df_filtrado.head())

        # Passo 3: Escolher os parâmetros para análise (exemplo: colunas)
        parameter_columns = st.multiselect(
            "Escolha os parâmetros para análise:",
            options=df_filtrado.columns,
            default=df_filtrado.columns[:5]  # Por padrão, escolhe as primeiras 5 colunas
        )
        
        if parameter_columns:
            # Passo 4: Escolher o parâmetro para teste (se necessário)
            parametro_para_teste = st.text_input("Digite o nome do parâmetro para o teste", "Exemplo de parâmetro")

            # Passo 5: Escolher o diretório de saída (em um ambiente Streamlit, geralmente é só para download)
            pasta_saida = "gráficos_output"  # Não é necessário um diretório local, pois o Streamlit permite o download direto

            # Passo 6: Gerar gráficos e permitir download
            plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste, pasta_saida)
        
        else:
            st.warning("Selecione pelo menos um parâmetro para análise.")
    else:
        st.info("Carregue um arquivo CSV para começar a análise.")




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





def plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste, pasta_saida):  
    agora = dtt.datetime.now()
    agora = agora.strftime('%Y/%m/%d %H:%M:%S')
    
    # Encontrar as colunas que possuem "Amplitude" no nome (excluindo "Flag_")
    amplitude_cols = [col for col in df_filtrado.columns if "Amplitude" in col and "Flag_" not in col  and "GMT-03:00" not in col]
    speed_cols = [col for col in df_filtrado.columns if "Speed" in col and "Flag_" not in col  and "GMT-03:00" not in col]
    
    # Garantir que as colunas de "Amplitude" sejam numéricas, descartando valores não numéricos
    df_amplitude = df_filtrado[amplitude_cols].apply(pd.to_numeric, errors='coerce')
    df_speed = df_filtrado[speed_cols].apply(pd.to_numeric, errors='coerce')
    
    if not df_amplitude.empty:
        ymin_amplitude = df_amplitude.min().min() * 0.7
        ymax_amplitude = df_amplitude.max().max() * 1.3
    
    if not df_speed.empty:
        ymin_speed = df_speed.max().max() * -0.1
        ymax_speed = df_speed.max().max() * 1.1
    
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
            
            df_nan = df_filtrado[df_filtrado[param].isna()]
            df_nan = df_nan.fillna(df_filtrado.mean())

            count_flag_0 = len(df_flag_0)
            count_flag_4 = len(df_flag_4)
            porcentagem_flag_0 = round((count_flag_0 / len(df_filtrado)) * 100, 2)
            porcentagem_flag_4 = round((count_flag_4 / len(df_filtrado)) * 100, 2)
            
            plt.plot(df_filtrado['GMT-03:00'], df_filtrado[param], label=f'Série Completa: Flag 0 ({porcentagem_flag_0}%)', alpha=0.7, color='black', linestyle='-', linewidth=1, zorder=1)
            plt.scatter(df_flag_4['GMT-03:00'], df_flag_4[param], color='red', alpha=1, s=15, label=f'Flag 4 ({porcentagem_flag_4}%)', zorder=2)
            plt.plot(df_nan['GMT-03:00'], df_nan[param], alpha=0.8, color='black', linestyle='dotted', linewidth=1, label = 'Valores nulos', zorder=3)

            data_inicio = str(df_filtrado['GMT-03:00'].iloc[0])
            data_fim = str(df_filtrado['GMT-03:00'].iloc[-1])
            
            plt.title(f'Série Temporal: {parametro_para_teste} - {param} - execução do reporte: {agora}\nPeríodo de análise: {data_inicio} - {data_fim}')
            plt.xlabel('Tempo (Data/Hora)')
            
            # Ajustar o eixo Y
            if param in amplitude_cols:
                plt.ylim(ymin_amplitude, ymax_amplitude)
            elif param in speed_cols:
                plt.ylim(ymin_speed, ymax_speed)
            
            plt.legend(loc='upper right')
            plt.grid(True, linestyle='dotted', alpha=0.5)

            # Criar o gráfico em um objeto de memória
            img_bytes = io.BytesIO()
            plt.savefig(img_bytes, format='png')
            img_bytes.seek(0)  # Resetar o ponteiro do arquivo para o início

            # Criar um nome de arquivo seguro
            safe_param_name = param.replace(' ', '_').replace('(', '').replace(')', '').replace('#', '').replace('/', '_').replace('\\', '_').replace('*', '')
            safe_initial_date_name = data_inicio.replace(' ', '_').replace('(', '').replace(')', '').replace('#', '').replace('/', '_').replace('\\', '_').replace('*', '').replace(':', '')
            safe_final_date_name = data_fim.replace(' ', '_').replace('(', '').replace(')', '').replace('#', '').replace('/', '_').replace('\\', '_').replace('*', '').replace(':', '')

            # Usar o Streamlit para criar o botão de download
            st.download_button(
                label=f'Download do Gráfico {param}',
                data=img_bytes,
                file_name=f'{parametro_para_teste} - Flag_{safe_param_name} - {safe_initial_date_name} - {safe_final_date_name}.png',
                mime="image/png"
            )
            plt.close()
            
    print("\nREPORTE EM GRÁFICOS FINALIZADO.")

#%% Executando a função para exibir a página no Streamlit


def main():
    
   
    # Chamando a função do Streamlit para exibir a página
    exibir_pagina_streamlit()

# Chama a função principal se o arquivo for executado diretamente
if __name__ == "__main__":
    main()

