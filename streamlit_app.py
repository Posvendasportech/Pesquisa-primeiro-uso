import streamlit as st
import pandas as pd
from datetime import datetime
import gspread
from google.oauth2.service_account import Credentials
import os

# Config (adicione seu JSON key em secrets.toml)
@st.cache_resource
def load_sheet():
    scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
    creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open("Sportech_Quiz").sheet1  # Nome da sua planilha
    return sheet

st.set_page_config(page_title="Quiz Sportech", layout="wide")

st.title("🎯 Sua Experiência com Sportech")
st.markdown("---")

# Sidebar progresso
progress = st.sidebar.progress(0)
st.sidebar.markdown("**Clique e avance automaticamente!**")

# Formulário quiz
with st.form("sportech_quiz", clear_on_submit=True):
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 1. Como sentiu os adesivos?")
        sentimento = st.radio("", ["Muito bom ❤️", "Bom 😊", "Regular 🤔", "Não ajudou 😔"], key="sent1")
    
    with col2:
        st.markdown("### 2. Usou onde?")
        local = st.radio("", ["Joelho", "Ombro", "Coluna", "Pernas", "Outro"], key="local1")
    
    col3, col4 = st.columns(2)
    
    with col3:
        st.markdown("### 3. Como está usando?")
        utilizacao = st.radio("", ["Todo dia", "Algumas x/semana", "Ocasionalmente", "Parei"], key="util1")
    
    with col4:
        st.markdown("### 4. Sua experiência?")
        experiencia = st.text_area("", placeholder="Conte pra gente...", key="exp1")
    
    nome = st.text_input("Nome pra te chamar ❤️")
    telefone = st.text_input("WhatsApp (pra 10% OFF)")
    
    submit = st.form_submit_button("✨ Enviar & Receber 10% OFF!", use_container_width=True)

if submit:
    try:
        sheet = load_sheet()
        row = [datetime.now().strftime("%d/%m/%Y %H:%M"), nome, telefone, sentimento, local, utilizacao, experiencia]
        sheet.append_row(row)
        st.balloons()
        st.success(f"✅ Obrigada, {nome}! 10% OFF no WhatsApp em 1min!")
        st.balloons()
    except:
        st.error("Erro sheet - confira secrets.toml")

# Preview dados (últimas 10 linhas)
if st.button("Ver respostas na planilha"):
    try:
        df = pd.DataFrame(sheet.get_all_records())
        st.dataframe(df.tail(10))
    except:
        st.info("Configure Google Sheets primeiro")
