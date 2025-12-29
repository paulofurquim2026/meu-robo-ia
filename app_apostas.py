import pandas as pd
import sqlite3
import joblib
import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO E ELO ---
def inicializar_banco():
    conn = sqlite3.connect('sistema_apostas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rankings_elo 
                      (time TEXT PRIMARY KEY, pontuacao REAL)''')
    conn.commit()
    return conn

def calcular_kelly(p, b, banca):
    if b <= 1: return 0
    f_kelly = (p * (b - 1) - (1 - p)) / (b - 1)
    return max(0, f_kelly * 0.5) * banca  # Meio Kelly

# --- INTERFACE DO APLICATIVO (STREAMLIT) ---
st.set_page_config(page_title="IA Predictor Pro", layout="wide")
st.title("⚽ Robô de Análise Quantitativa v1.0")

menu = st.sidebar.selectbox("Menu", ["Analisar Jogo", "Rankings Elo", "Configurações"])

if menu == "Analisar Jogo":
    st.header("🔍 Nova Análise de Valor")
    
    col1, col2 = st.columns(2)
    with col1:
        time_h = st.text_input("Time da Casa")
        odd_h = st.number_input("Odd Casa", min_value=1.01, value=2.00)
    with col2:
        time_a = st.text_input("Time Visitante")
        banca = st.number_input("Sua Banca Atual (R$)", min_value=0.0, value=1000.0)

    if st.button("Gerar Palpite"):
        # Simulação de lógica (Aqui entraria seu modelo .pkl carregado)
        # Para o app funcionar agora, usaremos uma lógica de Elo baseada no banco
        conn = inicializar_banco()
        cursor = conn.cursor()
        
        # Busca elo ou define padrão 1500
        cursor.execute("SELECT pontuacao FROM rankings_elo WHERE time=?", (time_h,))
        elo_h = cursor.fetchone()
        elo_h = elo_h[0] if elo_h else 1500.0
        
        cursor.execute("SELECT pontuacao FROM rankings_elo WHERE time=?", (time_a,))
        elo_a = cursor.fetchone()
        elo_a = elo_a[0] if elo_a else 1500.0
        
        # Probabilidade baseada no diferencial de Elo
        prob_h = 1 / (1 + 10 ** ((elo_a - elo_h) / 400))
        ev = prob_h * odd_h
        
        st.divider()
        st.subheader(f"Resultado: {time_h} vs {time_a}")
        
        if ev > 1.10:
            sugestao = calcular_kelly(prob_h, odd_h, banca)
            st.success(f"✅ APOSTA DE VALOR DETECTADA!")
            st.write(f"**Probabilidade Calculada:** {prob_h*100:.1f}%")
            st.write(f"**Valor Esperado (EV):** {ev:.2f}")
            st.metric("Sugestão de Aposta", f"R$ {sugestao:.2f}")
        else:
            st.warning("⚠️ Sem valor matemático nesta odd.")

elif menu == "Rankings Elo":
    st.header("📊 Rankings de Força (Elo)")
    conn = inicializar_banco()
    df_elo = pd.read_sql_query("SELECT * FROM rankings_elo ORDER BY pontuacao DESC", conn)
    st.table(df_elo)import pandas as pd
import sqlite3
import joblib
import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO E ELO ---
def inicializar_banco():
    conn = sqlite3.connect('sistema_apostas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rankings_elo 
                      (time TEXT PRIMARY KEY, pontuacao REAL)''')
    conn.commit()
    return conn

def calcular_kelly(p, b, banca):
    if b <= 1: return 0
    f_kelly = (p * (b - 1) - (1 - p)) / (b - 1)
    return max(0, f_kelly * 0.5) * banca  # Meio Kelly

# --- INTERFACE DO APLICATIVO (STREAMLIT) ---
st.set_page_config(page_title="IA Predictor Pro", layout="wide")
st.title("⚽ Robô de Análise Quantitativa v1.0")

menu = st.sidebar.selectbox("Menu", ["Analisar Jogo", "Rankings Elo", "Configurações"])

if menu == "Analisar Jogo":
    st.header("🔍 Nova Análise de Valor")
    
    col1, col2 = st.columns(2)
    with col1:
        time_h = st.text_input("Time da Casa")
        odd_h = st.number_input("Odd Casa", min_value=1.01, value=2.00)
    with col2:
        time_a = st.text_input("Time Visitante")
        banca = st.number_input("Sua Banca Atual (R$)", min_value=0.0, value=1000.0)

    if st.button("Gerar Palpite"):
        # Simulação de lógica (Aqui entraria seu modelo .pkl carregado)
        # Para o app funcionar agora, usaremos uma lógica de Elo baseada no banco
        conn = inicializar_banco()
        cursor = conn.cursor()
        
        # Busca elo ou define padrão 1500
        cursor.execute("SELECT pontuacao FROM rankings_elo WHERE time=?", (time_h,))
        elo_h = cursor.fetchone()
        elo_h = elo_h[0] if elo_h else 1500.0
        
        cursor.execute("SELECT pontuacao FROM rankings_elo WHERE time=?", (time_a,))
        elo_a = cursor.fetchone()
        elo_a = elo_a[0] if elo_a else 1500.0
        
        # Probabilidade baseada no diferencial de Elo
        prob_h = 1 / (1 + 10 ** ((elo_a - elo_h) / 400))
        ev = prob_h * odd_h
        
        st.divider()
        st.subheader(f"Resultado: {time_h} vs {time_a}")
        
        if ev > 1.10:
            sugestao = calcular_kelly(prob_h, odd_h, banca)
            st.success(f"✅ APOSTA DE VALOR DETECTADA!")
            st.write(f"**Probabilidade Calculada:** {prob_h*100:.1f}%")
            st.write(f"**Valor Esperado (EV):** {ev:.2f}")
            st.metric("Sugestão de Aposta", f"R$ {sugestao:.2f}")
        else:
            st.warning("⚠️ Sem valor matemático nesta odd.")

elif menu == "Rankings Elo":
    st.header("📊 Rankings de Força (Elo)")
    conn = inicializar_banco()
    df_elo = pd.read_sql_query("SELECT * FROM rankings_elo ORDER BY pontuacao DESC", conn)
    st.table(df_elo)import pandas as pd
import sqlite3
import joblib
import streamlit as st
from datetime import datetime

# --- CONFIGURAÇÃO DO BANCO E ELO ---
def inicializar_banco():
    conn = sqlite3.connect('sistema_apostas.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS rankings_elo 
                      (time TEXT PRIMARY KEY, pontuacao REAL)''')
    conn.commit()
    return conn

def calcular_kelly(p, b, banca):
    if b <= 1: return 0
    f_kelly = (p * (b - 1) - (1 - p)) / (b - 1)
    return max(0, f_kelly * 0.5) * banca  # Meio Kelly

# --- INTERFACE DO APLICATIVO (STREAMLIT) ---
st.set_page_config(page_title="IA Predictor Pro", layout="wide")
st.title("⚽ Robô de Análise Quantitativa v1.0")

menu = st.sidebar.selectbox("Menu", ["Analisar Jogo", "Rankings Elo", "Configurações"])

if menu == "Analisar Jogo":
    st.header("🔍 Nova Análise de Valor")
    
    col1, col2 = st.columns(2)
    with col1:
        time_h = st.text_input("Time da Casa")
        odd_h = st.number_input("Odd Casa", min_value=1.01, value=2.00)
    with col2:
        time_a = st.text_input("Time Visitante")
        banca = st.number_input("Sua Banca Atual (R$)", min_value=0.0, value=1000.0)

    if st.button("Gerar Palpite"):
        # Simulação de lógica (Aqui entraria seu modelo .pkl carregado)
        # Para o app funcionar agora, usaremos uma lógica de Elo baseada no banco
        conn = inicializar_banco()
        cursor = conn.cursor()
        
        # Busca elo ou define padrão 1500
        cursor.execute("SELECT pontuacao FROM rankings_elo WHERE time=?", (time_h,))
        elo_h = cursor.fetchone()
        elo_h = elo_h[0] if elo_h else 1500.0
        
        cursor.execute("SELECT pontuacao FROM rankings_elo WHERE time=?", (time_a,))
        elo_a = cursor.fetchone()
        elo_a = elo_a[0] if elo_a else 1500.0
        
        # Probabilidade baseada no diferencial de Elo
        prob_h = 1 / (1 + 10 ** ((elo_a - elo_h) / 400))
        ev = prob_h * odd_h
        
        st.divider()
        st.subheader(f"Resultado: {time_h} vs {time_a}")
        
        if ev > 1.10:
            sugestao = calcular_kelly(prob_h, odd_h, banca)
            st.success(f"✅ APOSTA DE VALOR DETECTADA!")
            st.write(f"**Probabilidade Calculada:** {prob_h*100:.1f}%")
            st.write(f"**Valor Esperado (EV):** {ev:.2f}")
            st.metric("Sugestão de Aposta", f"R$ {sugestao:.2f}")
        else:
            st.warning("⚠️ Sem valor matemático nesta odd.")

elif menu == "Rankings Elo":
    st.header("📊 Rankings de Força (Elo)")
    conn = inicializar_banco()
    df_elo = pd.read_sql_query("SELECT * FROM rankings_elo ORDER BY pontuacao DESC", conn)
    st.table(df_elo)