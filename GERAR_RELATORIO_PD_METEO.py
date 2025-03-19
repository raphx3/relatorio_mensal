import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import datetime as dtt
import os

# Função para processar colunas e extrair dados numéricos
def processar_colunas_amplitude_speed(df_filtrado):
    amplitude_cols = [col for col in df_filtrado.columns if "Amplitude" in col and "Flag_" not in col  and "GMT-03:00" not in col]
    speed_cols = [col for col in df_filtrado.columns if "Speed" in col and "Flag_" not in col  and "GMT-03:00" not in col]
    
    df_amplitude = df_filtrado[amplitude_cols].apply(pd.to_numeric, errors='coerce')  
    df_speed = df_filtrado[speed_cols].apply(pd.to_numeric, errors='coerce')  

    return df_amplitude, df_speed, amplitude_cols, speed_cols

# Função para calcular limites do gráfico
def calcular_limites(df_amplitude, df_speed):
    if not df_amplitude.empty:
        ymin_amplitude = df_amplitude.min().min() * 0.7
        ymax_amplitude = df_amplitude.max().max() * 1.3
    else:
        ymin_amplitude, ymax_amplitude = None, None

    if not df_speed.empty:
        ymin_speed = df_speed.max().max() * -0.1
        ymax_speed = df_speed.max().max() * 1.1
    else:
        ymin_speed, ymax_speed = None, None

    return ymin_amplitude, ymax_amplitude, ymin_speed, ymax_speed

# Função para configurar os rótulos do eixo Y de acordo com o parâmetro
def configurar_rotulos(param):
    rotulos = {
        "Amplitude": "Amplitude (m)",
        "Speed": "Velocidade (m/s)",
        "Direction": "Direção (°)",
        "Roll": "Direção (°)",
        "Heading": "Direção (°)",
        "Pitch": "Direção (°)",
        "Temperature": "Temperatura (°C)",
        "Pressure": "Pressão (dbar)",
        "Battery": "Tensão (Volts)",
        "Rain": "Altura (mm)",
        "Wind Direction(*)": "Direção (°)",
        "Gust Speed(m/s)": "Velocidade (m/s)",
        "Wind Speed(m/s)": "Velocidade (m/s)",
        "Dew Point": "Temperatura (°C)",
        "RH(%)": "Umidade (%)",
        "Tide_Level": "Altura (m)",
        "Sensor_Velki": "Altura (m)",
        "CutOff_Freq_High": "Frequência (n/s)",
        "Peak_Period": "Período (s)",
        "Max_Height": "Altura (m)",
        "Sign_Height": "Altura (m)"
    }

    for chave in rotulos:
        if chave in param:
            return rotulos[chave]
    return "Valor"

# Função para garantir que o eixo X tenha 5 ticks igualmente espaçados
def configurar_ticks_x(df_filtrado):
    time_min = df_filtrado['GMT-03:00'].min()
    time_max = df_filtrado['GMT-03:00'].max()
    time_min_timestamp = time_min.timestamp()
    time_max_timestamp = time_max.timestamp()

    xticks_positions_timestamp = np.linspace(time_min_timestamp, time_max_timestamp, 5)
    xticks_positions = [pd.to_datetime(ts, unit='s') for ts in xticks_positions_timestamp]

    return xticks_positions

#%% plot_series_temporais
def plot_series_temporais(df_filtrado, parameter_columns, parametro_para_teste, pasta_saida):  
    agora = dtt.datetime.now()
    agora = agora.strftime('%Y/%m/%d %H:%M:%S')
    
    df_amplitude, df_speed, amplitude_cols, speed_cols = processar_colunas_amplitude_speed(df_filtrado)
    ymin_amplitude, ymax_amplitude, ymin_speed, ymax_speed = calcular_limites(df_amplitude, df_speed)

    for param in parameter_columns:
        flag_column = f'Flag_{param}'
        
        if flag_column in df_filtrado.columns:
            plt.figure(figsize=(12, 6))
            plt.gca().set_facecolor('white')

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
            plt.plot(df_nan['GMT-03:00'], df_nan[param], alpha=0.8, color='black', linestyle='dotted', linewidth=1, label='Valores nulos', zorder=3)
            
            data_inicio = str(df_filtrado['GMT-03:00'].iloc[0])
            data_fim = str(df_filtrado['GMT-03:00'].iloc[-1])
            
            plt.title(f'Série Temporal: {parametro_para_teste} - {param} - execução do reporte: {agora}\nPeríodo de análise: {data_inicio} - {data_fim}')
            plt.xlabel('Tempo (Data/Hora)')
            plt.ylabel(configurar_rotulos(param))
            
            xticks_positions = configurar_ticks_x(df_filtrado)
            plt.xticks(xticks_positions, rotation=0)

            if param in amplitude_cols:
                plt.ylim(ymin_amplitude, ymax_amplitude)
                plt.yticks(np.linspace(ymin_amplitude, ymax_amplitude, 6))  # Garantir 5 ticks
            elif param in speed_cols:
                plt.ylim(ymin_speed, ymax_speed)
                plt.yticks(np.linspace(ymin_speed, ymax_speed, 6))  # Garantir 5 ticks

            plt.legend(loc='upper right')
            plt.grid(True, linestyle='dotted', alpha=0.5)

            os.makedirs(pasta_saida, exist_ok=True)

            safe_param_name = param.replace(' ', '_').replace('(', '').replace(')', '').replace('#', '').replace('/', '_').replace('\\', '_').replace('*', '')
            safe_initial_date_name = data_inicio.replace(' ', '_').replace('(', '').replace(')', '').replace('#', '').replace('/', '_').replace('\\', '_').replace('*', '').replace(':', '')
            safe_final_date_name = data_fim.replace(' ', '_').replace('(', '').replace(')', '').replace('#', '').replace('/', '_').replace('\\', '_').replace('*', '').replace(':', '')

            plt.savefig(os.path.join(pasta_saida, f'{parametro_para_teste} - Flag_{safe_param_name} - {safe_initial_date_name} - {safe_final_date_name}.png'))
            plt.close()

    print("\nREPORTE EM GRÁFICOS FINALIZADO.")

#%% Executando a função para exibir a página no Streamlit
def main():
    exibir_pagina_streamlit()

# Chama a função principal se o arquivo for executado diretamente
if __name__ == "__main__":
    main()
