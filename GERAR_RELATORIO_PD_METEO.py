import os
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import datetime as dtt
import io
import streamlit as st

# Função para exibir a página no Streamlit
def exibir_pagina_streamlit():
    st.title("Relatório de Séries Temporais")
    
    # Exibição de campos de entrada no Streamlit
    pasta_saida = st.text_input(
        'Insira o caminho da pasta onde os resultados serão salvos:', 
        r'C:\Users\Rafael Alvarenga UMI\Desktop\PD_METEO\REPORTES\RELATORIO_MENSAL\RESULTADOS',
        key='input_pasta_saida'
    )
    
    # Botão para gerar os gráficos
    if st.button('Gerar Gráficos'):
        # A seguir, chamaremos a função plot_series_temporais
        df_filtrado = pd.DataFrame()  # Suponha que você tenha um DataFrame já carregado
        parameter_columns = ['Amplitude', 'Speed', 'Temperature']  # Exemplos de parâmetros
        parametro_para_teste = 'Exemplo de Teste'
        
        plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste, pasta_saida)

# Função para filtrar dados por período (se necessário, você pode adaptá-la)
def filtrar_por_periodo(df, inicio, fim):
    return df[(df['GMT-03:00'] >= inicio) & (df['GMT-03:00'] <= fim)]

# Função para gerar os gráficos das séries temporais
def plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste, pasta_saida):
    agora = dtt.datetime.now()
    agora = agora.strftime('%Y/%m/%d %H:%M:%S')

    # Encontrar as colunas que possuem "Amplitude" no nome (excluindo "Flag_")
    amplitude_cols = [col for col in df_filtrado.columns if "Amplitude" in col and "Flag_" not in col and "GMT-03:00" not in col]
    speed_cols = [col for col in df_filtrado.columns if "Speed" in col and "Flag_" not in col and "GMT-03:00" not in col]
    
    # Garantir que as colunas de "Amplitude" sejam numéricas, descartando valores não numéricos
    df_amplitude = df_filtrado[amplitude_cols].apply(pd.to_numeric, errors='coerce')
    df_speed = df_filtrado[speed_cols].apply(pd.to_numeric, errors='coerce')
    
    # Calcular os limites globais do eixo Y com base nas colunas "Amplitude"
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
            
            # Contagem de dados por flags
            count_flag_0 = len(df_flag_0)
            count_flag_4 = len(df_flag_4)
            porcentagem_flag_0 = round((count_flag_0 / len(df_filtrado)) * 100, 2)
            porcentagem_flag_4 = round((count_flag_4 / len(df_filtrado)) * 100, 2)
            
            # Plotar série completa
            plt.plot(df_filtrado['GMT-03:00'], df_filtrado[param], label=f'Série Completa: Flag 0 ({porcentagem_flag_0}%)', alpha=0.7, color='black', linestyle='-', linewidth=1, zorder=1)

            # Plotar os dados com Flag 4 (vermelho) como pontos
            plt.scatter(df_flag_4['GMT-03:00'], df_flag_4[param], color='red', alpha=1, s=15, label=f'Flag 4 ({porcentagem_flag_4}%)', zorder=2)
            
            # Plotar os nan como a média da série temporal
            plt.plot(df_nan['GMT-03:00'], df_nan[param], alpha=0.8, color='black', linestyle='dotted', linewidth=1, label = 'Valores nulos', zorder=3)

            # Configurações do gráfico
            data_inicio = str(df_filtrado['GMT-03:00'].iloc[0])
            data_fim = str(df_filtrado['GMT-03:00'].iloc[-1])
            
            plt.title(f'Série Temporal: {parametro_para_teste} - {param} - execução do reporte: {agora}\nPeríodo de análise: {data_inicio} - {data_fim}')
            plt.xlabel('Tempo (Data/Hora)')
            
            # Definir o eixo Y conforme o tipo de parâmetro
            if "Amplitude" in param:
                plt.ylabel('Amplitude (m)')
            if "Speed" in param:
                plt.ylabel('Velocidade (m/s)')
            if "Temperature" in param:
                plt.ylabel('Temperatura (°C)')
            if "Pressure" in param:
                plt.ylabel('Pressão (dbar)')

            # Garantir que o eixo X tenha sempre 5 ticks
            time_min = df_filtrado['GMT-03:00'].min()
            time_max = df_filtrado['GMT-03:00'].max()
            time_min_timestamp = time_min.timestamp()
            time_max_timestamp = time_max.timestamp()

            xticks_positions_timestamp = np.linspace(time_min_timestamp, time_max_timestamp, 5)
            xticks_positions = [pd.to_datetime(ts, unit='s') for ts in xticks_positions_timestamp]
            plt.xticks(xticks_positions, rotation=0)

            # Definir limites do eixo Y
            if param in amplitude_cols:
                plt.ylim(ymin_amplitude, ymax_amplitude)
            if param in speed_cols:
                plt.ylim(ymin_speed, ymax_speed)

            plt.legend(loc='upper right')
            plt.grid(True, linestyle='dotted', alpha=0.5)
            
            # Salvar o gráfico para o Streamlit (não em um diretório)
            img_stream = io.BytesIO()
            plt.savefig(img_stream, format='png')
            img_stream.seek(0)  # Rewind the image stream

            # Utilizar o download_button para permitir o download da imagem gerada
            file_name = f'{parametro_para_teste} - Flag_{param} - {data_inicio} - {data_fim}.png'
            st.download_button(
                label=f'Download do gráfico: {file_name}',
                data=img_stream,
                file_name=file_name,
                mime="image/png"
            )
            plt.close()

    print("\nREPORTE EM GRÁFICOS FINALIZADO.")

# Função principal
def main():
    # Chamando a função do Streamlit para exibir a página
    exibir_pagina_streamlit()

if __name__ == "__main__":
    main()
