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
    st.title('Relatório mensal')
    
    # Campos para o usuário inserir informações de configuração de teste
    analista = st.text_input('Nome do Analista:', 'Raphael')  # Nome do analista
    projeto = st.text_input('Nome do Projeto:', 'PD_METEO')  # Nome do projeto
    boia = st.text_input('Nome da Boia:', 'Protótipo 1')  # Nome da boia
    #parametro_para_teste = st.text_input('Selecione o parâmetro para teste:')  # Nome da boia
    
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

    # Campo para o usuário inserir o caminho da pasta onde os resultados serão salvos
    pasta_saida = st.text_input(
        'Insira o caminho da pasta onde os resultados serão salvos:', 
        r'C:\Users\Rafael Alvarenga UMI\Desktop\PD_METEO\REPORTES\RELATORIO_MENSAL\RESULTADOS',
        key='input_pasta_saida'
    )

    # Botão para gerar os resultados e salvar na pasta
    if st.button(label='Gerar Resultados para Relatório na Pasta Selecionada'):
        if pasta_saida:
            # Verifica se o diretório existe, se não, cria o diretório
            try:
                os.makedirs(pasta_saida, exist_ok=True)  # Cria o diretório se não existir
                st.success(f"Pasta criada em: {pasta_saida}")
            except Exception as e:
                st.error(f"Erro ao criar a pasta: {e}")
                return

            # Exibir a barra de progresso
            progress_bar = st.progress(0)
            progress_text = st.empty()

            # Filtrando dados por parametro
            try:
                # Primeira etapa: Filtrando os dados (0% - 25%)
                progress_text.text("Filtrando dados...")
                for i in range(1, 26):  # Vai de 0% até 25%
                    progress_bar.progress(i)
                    time.sleep(0.1)  # Espera 1 segundo a cada incremento                 
                    
                if 'CORRENTES' in parametro_para_teste:
                    parameter_columns=parameter_columns_correntes
                    #df_correntes,parameter_columns=importar_dados_corrente_string_ADCP(df_PNORC,df_PNORI,df_PNORS,parameter_columns_PNORC,parameter_columns_PNORI,parameter_columns_PNORS,parameter_columns)
                    #df_correntes= aplicar_filtros(df_correntes,parameter_columns,dict_offset, limites_range_check, dict_max_min_test, st_time_series_dict, limite_repeticao_dados, limite_sigma_aceitavel_and_dict_delta_site, sampling_frequency, coluna_tempo, alert_window_size, dict_spike,dict_lt_time_and_regressao)
                    df=df_correntes

                
                if 'METEOROLOGIA' in parametro_para_teste:
                    parameter_columns=parameter_columns_meteo
                    #df_meteo, nomes_colunas = import_df_meteo(input_file_meteo, nomes_colunas=parameter_columns_meteo)
                    #df_meteo= aplicar_filtros(df_meteo,parameter_columns,dict_offset, limites_range_check, dict_max_min_test, st_time_series_dict, limite_repeticao_dados, limite_sigma_aceitavel_and_dict_delta_site, sampling_frequency, coluna_tempo, alert_window_size, dict_spike,dict_lt_time_and_regressao)
                    df=df_meteo

                
                if 'MARE' in parametro_para_teste:
                    parameter_columns=parameter_columns_mare
                    #df_tide,nomes_colunas= import_df_mare(input_file_mare, nomes_colunas=parameter_columns_mare)
                    #df_tide= aplicar_filtros(df_tide, parameter_columns, dict_offset, limites_range_check, dict_max_min_test, st_time_series_dict, limite_repeticao_dados, limite_sigma_aceitavel_and_dict_delta_site, sampling_frequency, coluna_tempo, alert_window_size, dict_spike,dict_lt_time_and_regressao)
                    df=df_tide

                
                if 'ONDAS' in parametro_para_teste:
                    parameter_columns=parameter_columns_ondas
                    #df_ondas = process_wave_data(df_PNORW, df_PNORB, df_PNORI, df_PNORS,parameter_columns_PNORW, parameter_columns_PNORB, parameter_columns_PNORI, parameter_columns_PNORS, parameter_columns_ondas)
                    #df_ondas= aplicar_filtros(df_ondas,parameter_columns,dict_offset, limites_range_check, dict_max_min_test, st_time_series_dict, limite_repeticao_dados, limite_sigma_aceitavel_and_dict_delta_site, sampling_frequency, coluna_tempo, alert_window_size, dict_spike,dict_lt_time_and_regressao)
                    df=df_ondas

                          
                if 'ONDAS_NAO_DIRECIONAIS' in parametro_para_teste:
                        parameter_columns=parameter_columns_ondas_nao_direcionais                    
                        #df_ondas_nao_direcionais = pd.read_csv(input_file_ondas_nao_direcionais,header=1,sep=',',names=parameter_columns_ondas_nao_direcionais)
                        #df_ondas_nao_direcionais.rename(columns={"TIMESTAMP": "GMT-03:00"}, inplace=True)
                        #for coluna in df_ondas_nao_direcionais.columns:
                            #df_ondas_nao_direcionais[f'Flag_{coluna}'] = 0
                        #df_ondas_nao_direcionais,resultados=aplicar_filtros(df_ondas_nao_direcionais, parameter_columns, dict_offset, limites_range_check, dict_max_min_test, st_time_series_dict, limite_repeticao_dados, limite_sigma_aceitavel_and_dict_delta_site, sampling_frequency, coluna_tempo, alert_window_size, dict_spike, dict_lt_time_and_regressao)
                        df=df_ondas_nao_direcionais
                    
                      
                # Filtragem dos dados por tempo
                df_filtrado_por_tempo, inicio, fim = filtrar_por_periodo(df, data_inicio, data_fim)
            
                # Segunda etapa: Processando dados (25% - 75%)
                progress_text.text("Processando dados...")
                for i in range(26, 76):  # Vai de 25% até 75%
                    progress_bar.progress(i)
                    time.sleep(0.1)  # Espera 1 segundo a cada incremento
                
             
                
                plot_series_temporais(df_filtrado_por_tempo, parameter_columns, parametro_para_teste, os.path.join(pasta_saida, parametro_para_teste))
            
                # Terceira etapa: Gerando o relatório (75% - 100%)
                progress_text.text("Gerando o relatório...")
                for i in range(76, 101):  # Vai de 75% até 100%
                    progress_bar.progress(i)
                    time.sleep(0.1)  # Espera 1 segundo a cada incremento
                progress_text.text("Processo finalizado.")
                
                # Finalizando o processo
                output_file = os.path.join(pasta_saida)
                st.success(f"Relatório gerado com sucesso em: {output_file}\{parametro_para_teste}")
            
            except Exception as e:
                st.error(f"Erro ao gerar os resultados: {e}")
                progress_text.text("Erro durante o processo.")


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

