import pandas as pd
import streamlit as st
import scipy.stats
import time

# Inicializar variables de estado si aún no existen
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(columns=['No', 'Intentos', 'Media'])

st.header("Lanzar una moneda")

# Gráfico inicial
chart = st.line_chart([0.5])

def toss_coin(n):
    # Simulación de lanzaminetos: 0 = cruz, 1 = cara
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    mean = None
    outcome_no = 0
    outcome_1_count = 0

    # Progresión de la media a medida que se lanzan más monedas
    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1
        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05) # Simula el tiempo de procesamiento
    
    return mean

# Control deslizante para definir la cantidad de lanzamientos
number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)

# Botón para iniciar el experimento
start_button = st.button("Ejecutar")

if start_button:
    st.session_state['experiment_no'] += 1  # Incrementa el número de experimento
    st.write(f'Experimento {st.session_state["experiment_no"]} con {number_of_trials} intentos en curso.')

    # Realizar experimento y calcular media
    mean = toss_coin(number_of_trials)

    # Guardar resultados en el DataFrame
    new_result = pd.DataFrame({
        'No': [st.session_state['experiment_no']],
        'Intentos': [number_of_trials],
        'Media': [mean]
    })

    # Concatenar y eliminar índice anterior
    st.session_state['df_experiment_results'] = pd.concat(
        [st.session_state['df_experiment_results'], new_result], 
        ignore_index=True
    ).reset_index(drop=True)

# Mostrar tabla de resultados
st.subheader('Resultados de los experimentos')
st.write(st.session_state['df_experiment_results'])