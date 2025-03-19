import io
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import streamlit as st
import datetime as dtt
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

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

# Função principal para exibir o Streamlit
def main():
    st.title('Visualização de Séries Temporais')
    
    # Carregar os dados (df_filtrado, parameter_columns, etc.)
    # Aqui você deve ter o dataframe e os parâmetros configurados, vou usar um exemplo genérico para esse caso:
    
    # Exemplo de dados (substitua com os seus dados reais)
    df_filtrado_por_tempo = pd.DataFrame({
        'GMT-03:00': pd.date_range(start='2023-01-01', periods=100, freq='D'),
        'Amplitude_S1': np.random.rand(100) * 10,
        'Speed_S1': np.random.rand(100) * 20,
        'Flag_Amplitude_S1': np.random.choice([0, 4], size=100),
        'Flag_Speed_S1': np.random.choice([0, 4], size=100),
    })
    parameter_columns = ['Amplitude_S1', 'Speed_S1']  # Exemplos de colunas
    parametro_para_teste = 'ExemploTeste'  # Nome do parâmetro de teste
    
    # Gerar o gráfico em memória
    buf = plot_series_temporais(df_filtrado_por_tempo, parameter_columns, parametro_para_teste)
    
    # Exibir o botão de download
    st.download_button(
        label="Baixar Gráfico",
        data=buf,
        file_name="grafico_serie_temporal.png",
        mime="image/png"
    )

if __name__ == "__main__":
    main()
