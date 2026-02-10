import streamlit as st
import pandas as pd
from datetime import datetime
import os

# Config página
st.set_page_config(page_title="Quiz Sportech", page_icon="❤️", layout="centered")

# CSS customizado (design clean idosos)
st.markdown("""
<style>
    .main {background: linear-gradient(135deg, #f4f7fa, #e8f0fe);}
    h1 {color: #2c5aa0; text-align: center;}
    .stRadio > label {font-size: 18px; font-weight: bold;}
    .stTextArea textarea {font-size: 16px;}
</style>
""", unsafe_allow_html=True)

# Inicializa dados
if 'respostas' not in st.session_state:
    if os.path.exists('respostas_sportech.csv'):
        st.session_state.respostas = pd.read_csv('respostas_sportech.csv')
    else:
        st.session_state.respostas = pd.DataFrame(columns=[
            'Data', 'Nome', 'Telefone', 'Sentimento_Adesivos', 
            'Local_Usado', 'Forma_Utilizacao', 'Experiencia_Sportech'
        ])

# Header
st.title("🎯 Sua Experiência com a Sportech")
st.markdown("### Responda e ganhe **10% OFF** no próximo pedido! 💚")
st.markdown("---")

# Formulário quiz
with st.form("quiz_sportech", clear_on_submit=True):
    
    # Pergunta 1
    st.markdown("#### 1. Como você sentiu utilizando os adesivos?")
    sentimento = st.radio(
        "",
        ["Muito bom, aliviou bastante ❤️", 
         "Bom, ajudou um pouco 😊", 
         "Regular, esperava mais 🤔", 
         "Não ajudou como esperava 😔"],
        key="sent",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Pergunta 2
    st.markdown("#### 2. Você usou onde? (principal)")
    local = st.radio(
        "",
        ["Joelho", "Ombro", "Coluna/Lombar", "Pernas", "Outro"],
        key="local",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Pergunta 3
    st.markdown("#### 3. Como você está utilizando?")
    utilizacao = st.radio(
        "",
        ["Todo dia", "Algumas vezes por semana", "Ocasionalmente", "Parei de usar"],
        key="util",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Pergunta 4
    st.markdown("#### 4. Me conte um pouquinho como está sendo sua experiência com a Sportech:")
    experiencia = st.text_area(
        "",
        placeholder="Ex: 'Adorei o produto, mas ainda sinto um pouquinho de dor...'",
        height=120,
        key="exp",
        label_visibility="collapsed"
    )
    
    st.markdown("---")
    
    # Dados pessoais
    col1, col2 = st.columns(2)
    with col1:
        nome = st.text_input("📝 Seu nome:", placeholder="João Silva")
    with col2:
        telefone = st.text_input("📱 WhatsApp/Telefone:", placeholder="(31) 99999-9999")
    
    # Botão submit
    submitted = st.form_submit_button("✨ Enviar e Receber 10% OFF!", use_container_width=True)

# Processa submissão
if submitted:
    if nome and telefone and experiencia:
        # Cria nova linha
        nova_resposta = pd.DataFrame({
            'Data': [datetime.now().strftime("%d/%m/%Y %H:%M:%S")],
            'Nome': [nome],
            'Telefone': [telefone],
            'Sentimento_Adesivos': [sentimento],
            'Local_Usado': [local],
            'Forma_Utilizacao': [utilizacao],
            'Experiencia_Sportech': [experiencia]
        })
        
        # Adiciona aos dados
        st.session_state.respostas = pd.concat([st.session_state.respostas, nova_resposta], ignore_index=True)
        
        # Salva CSV
        st.session_state.respostas.to_csv('respostas_sportech.csv', index=False)
        
        # Feedback sucesso
        st.balloons()
        st.success(f"✅ **Obrigada, {nome}!** Seu cupom de 10% OFF será enviado no WhatsApp em instantes! 🎉")
        st.info("💡 **Equipe Sportech:** Entraremos em contato pelo número cadastrado.")
        
    else:
        st.error("⚠️ Por favor, preencha nome, telefone e experiência!")

# Sidebar - Admin (visualização)
st.sidebar.title("📊 Painel Admin")
if st.sidebar.checkbox("Mostrar respostas", value=False):
    st.sidebar.markdown("---")
    st.sidebar.markdown(f"**Total respostas:** {len(st.session_state.respostas)}")
    
    if len(st.session_state.respostas) > 0:
        # Preview últimas 5
        st.subheader("📋 Últimas 5 Respostas")
        st.dataframe(st.session_state.respostas.tail(5), use_container_width=True)
        
        # Download CSV
        csv = st.session_state.respostas.to_csv(index=False).encode('utf-8-sig')
        st.download_button(
            label="📥 Baixar Planilha Completa (CSV)",
            data=csv,
            file_name=f'sportech_quiz_{datetime.now().strftime("%d%m%Y")}.csv',
            mime='text/csv',
            use_container_width=True
        )
        
        # Estatísticas rápidas
        st.subheader("📈 Estatísticas Rápidas")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Respostas", len(st.session_state.respostas))
        
        with col2:
            if len(st.session_state.respostas) > 0:
                local_mais_usado = st.session_state.respostas['Local_Usado'].mode()[0]
                st.metric("Local + Usado", local_mais_usado)
        
        with col3:
            if len(st.session_state.respostas) > 0:
                satisfacao = st.session_state.respostas['Sentimento_Adesivos'].str.contains('Muito bom|Bom').sum()
                taxa = f"{(satisfacao/len(st.session_state.respostas)*100):.0f}%"
                st.metric("Satisfação", taxa)
    else:
        st.info("Nenhuma resposta ainda.")

# Footer
st.markdown("---")
st.markdown(
    "<p style='text-align: center; color: #888;'>❤️ Feito com carinho pela Sportech | Cuidando do seu bem-estar</p>", 
    unsafe_allow_html=True
)
