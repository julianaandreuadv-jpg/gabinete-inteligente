import streamlit as st

# Configuração da página inteira (deve ser o primeiro comando)
st.set_page_config(
    page_title="Gabinete Inteligente | Alta Performance",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ Ecossistema Jurídico - Gabinete de Alta Performance")
st.markdown("Bem-vindo ao sistema de automação e gestão estratégica para Assessoria Judicial (Vara Única).")

st.markdown("---")

st.info("👈 **Para começar, insira sua Chave de API no menu lateral e selecione a competência desejada.**")

# Autenticação Global no Menu Lateral
st.sidebar.title("🔐 Autenticação")
api_key = st.sidebar.text_input("Chave API do Google Gemini:", type="password")

if api_key:
    # Salvamos a chave na "sessão" para que as outras páginas (Cível, Criminal) possam usar
    st.session_state['api_key'] = api_key
    st.sidebar.success("Sistema conectado. IA Pronta.")
else:
    st.sidebar.warning("Aguardando credenciais para habilitar os módulos.")
    
st.markdown("""
### 🏛️ Módulos Disponíveis (Via Menu Lateral):
* **📊 Orquestrador CNJ:** Gestão de filas, KPIs e alertas legais.
* **⚖️ Cível e Fazenda:** Sentenças, tutelas de urgência e liquidação.
* **🚨 Criminal e Júri:** Dosimetria trifásica, prisões e pronúncia.
* **🛡️ Violência Doméstica:** Medidas protetivas e cronogramas Maria da Penha.
* **👶 Infância e ECA:** Conhecimento e execução socioeducativa.
* **🗺️ Navegador de Ritos:** Mapa visual de processos (Máquinas de Estado).
""")
